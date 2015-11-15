#!/usr/bin/env python

"""
Implementation of a simple indexed table type.
"""
import types, re, os.path, codecs, time
True = 1
False = 0
class Table:

    def __init__(self, name, tableDef):
        self.__name = name
        self.__tableDef = tableDef
        self.__dict = {}
        self.__indexes = {}
        self.__regexpes = {}
        for index in tableDef.indexes + tableDef.unique_indexes:
            self.__indexes[tableDef.alias + "_" + index] = {}

            
    def getName(self):
        return self.__name

    def get(self, pk):
        return self.__dict[pk]


    def insert(self, dbRecord):
        
        pk = dbRecord.getPrimaryKey()
        if pk == None:
            try:
                pk = max(self.__dict.keys()) + 1
            except ValueError, e:
                if len(self.__dict.keys()) == 0:
                    pk = 1
                else:
                    raise e
            dbRecord.setPrimaryKey(pk)
        
        if self.__dict.has_key(pk):
            raise "Duplicate entry: " + str(dbRecord)
        if dbRecord.tableDef.fields.has_key("datestamp"):
            dbRecord.datestamp = time.time()
            
        self.__dict[pk] = dbRecord.getOwnerFields()
        
        # Add non-unique indexes
        for index in self.__tableDef.indexes:
            v = dbRecord.getFieldValue(index)
            #print "Adding non-unique index", index, "with value", v
            self.__indexes.setdefault(index, {}).setdefault(v, {})[pk] \
                                             = self.__dict[pk]
        
        # Add unique indexes        
        for index in self.__tableDef.unique_indexes:
            #print "Adding unique index", index, "with value", v
            v = dbRecord.getFieldValue(index)
            self.__indexes.setdefault(index, {}).setdefault(v, self.__dict[pk])


    def update(self, dbRecord):
        """
        Update a single record with the values in dbRecord
        """
        pk = dbRecord.getPrimaryKey()
        if pk == None:
            raise "Empty primary key not allowed: " + str(dbRecord)
        self.__delete(pk)
        self.insert(dbRecord)


    def __delete(self, pk):
        oldRecord = self.__dict[pk]

        # clear old non-unique indexes
        for index in self.__tableDef.indexes:
            v = oldRecord[index]
            set = self.__indexes[index][v]
            if set != None:
                if pk in set.keys():
                    del set[pk]
            
        # clear old unique indexes
        for index in self.__tableDef.unique_indexes:
            v = oldRecord[index]
            del self.__indexes[index][v]

        # remove record
        del self.__dict[pk]


    def delete(self, dbRecord):
        records = self.select(dbRecord)
        for record in records:
            pk = record[self.__tableDef.primarykey]
            self.__delete(pk)


    def __regexpify(self, s):
        #print "regexp on %s " % s
        if s not in self.__regexpes.keys():
            s2 = re.escape(s)
            s2 = "^" + s2
            s2 = s2 + "$"
            s2 = s2.replace(r"\%", ".*")
            r = re.compile(s2)
            self.__regexpes[s] = r
        r = self.__regexpes[s]
        #print "regexp: ", r.pattern
        return r

    def __check(self, dbRecord, record):
        """
        Check individual fields. 
        """
        #print "__check", record
        for k, v in record.items():
            v2 = dbRecord.getFieldValue(k)
            #print "\tChecking k, v with target", k, v, v2
            if v2 == None:
                continue
            if type(v2) in [types.StringType, types.UnicodeType]:
                if v2.find("%") > -1:
                    regexp = self.__regexpify(v2)
                    #print "\t\tMatching", regexp.pattern, v2
                    if regexp.match(v) == None:
                        #print "\t\t\tMatch missed"
                        return False
                    else:
                        #print "\t\t\tMatched"
                        continue
            #print "\t\tFinished checking", v2, v
            if v2 != None and v2 != "" and v2 != v:
                #print "\tCheck failed"
                return False
        #print "\tCheck success"
        return True

    def __checkFullTableScan(self, dbRecord):
        # check whether there is any selection
        for value in dbRecord.getFields().values():
            if value != None:
                #print "No full table copy"
                return False

        #print "Full table copy"
        return True

    def __selectByUniqueIndex(self, dbRecord):
        for unique_index in self.__tableDef.unique_indexes:
            #print "Checking unique index", unique_index
            unique_value = dbRecord.getFieldValue(unique_index)
            if unique_value != None:
                #print "Taking unique index", unique_index
                r = self.__indexes.get(unique_index).get(unique_value)
                if r == None:
                    raise "No record where " + unique_index + " = " \
                          + dbRecord.getFieldValue(unique_index)
                else:
                    if self.__check(dbRecord, r):
                        return [r]
        return []
    
    def __selectByIndex(self, dbRecord):
        resultSet = []
        sets = {}
        # Search by index
        index_value = None
        for index in self.__tableDef.indexes:
            #print "Checking index", index
            index_value = dbRecord.getFieldValue(index)
            if index_value == None:
                #print "\tNo query on this index"
                continue
            if type(index_value) in [types.StringType, types.UnicodeType]:
                if index_value.find("%") != -1:
                    #print "\tQuery on index %s contains wildcards" % index_value
                    continue
        
            # These indexes are not unique: so more than one
            # record can be indexed by this value
            #print "\tRetrieving set for query value, ", index_value
            i = self.__indexes.get(index)
            if i == None:
                #print "\t\tRetrieved no index for", index
                return ([], True)
            set = i.get(index_value)
            if set == None:
                #print "\t\tRetrieved no value for query", index_value, "on index", index
                return ([], True)
            else:
                #print "\t\t", len(set), "candidates for query", index_value, "on index", index
                sets[len(set)] = set
                

        if len(sets) > 0:
            # Select the smallest resultset
            smallestSet = min(sets.keys())
            #print "\t\tMinimal set has", smallestSet, "entries"
            for r in sets[smallestSet].values():
                if self.__check(dbRecord, r):
                    #print "\t\t\tRecord checks out ok"
                    resultSet.append(r)

            return (resultSet, True)
        return ([], False)

    def __internalSelect(self, dbRecord):
        #print "Complex select on ", self.__name, "using", dbRecord
        
        if self.__checkFullTableScan(dbRecord):
            return self.__dict.values()
        

        resultSet = self.__selectByUniqueIndex(dbRecord)

        if resultSet != []:
            return resultSet

        (resultSet, index_used) = self.__selectByIndex(dbRecord)
        
        if  index_used:
            # We have had a chance to find something by index, but
            # failed. A full table scan is useless now.
            return resultSet
        
        # If the resultset is still empty, we will do a full-table scan
        #print "Full table scan"
        for k, v in self.__dict.items():
            #print "Checking", k, v
            if self.__check(dbRecord, v):
                resultSet.append(v)

        return resultSet

    def select(self, dbRecord):
        pk = dbRecord.getPrimaryKey()

        if pk == None:
            return self.__internalSelect(dbRecord)
        else:
            record = self.__dict.get(pk)
            if record == None:
                raise "No record in table %s with primary key %s " % (self.__name, str(pk))
            else:
                return [record]
            
    def __repr__(self):
        return repr(self.__dict)

    def __len__(self):
        return len(self.__dict)


