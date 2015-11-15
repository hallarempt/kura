False = 0
True = 1

from qt import *

from guilistbox import guiListBox
from guicombobox import guiComboBox
from guinumberbox import guiNumberBox
from guimultilineedit import guiMultiLineEdit
from guicheckbox import guiCheckBox
from guilabel import guiLabel
from guilineedit import guiLineEdit
from guiconfig import guiConf

font = QFont(guiConf.textfontfamily, guiConf.textfontsize)

import constants

from dbobj.dbtypes import *

class FieldError(Exception):
    
    def __init__(self, field):
        Exception.__init__(self)
        self.field=field
        
    def __repr__(self):
        return "FieldError %s" % self.field

class guiForm(QWidget):
    """
    Generic layout managed form that can show all the fields in a record
    in the right format with the right initial values. This form can be used
    in any layoutmanager.
    """
    def __init__(self, parent, record, mode, *args):
        QWidget.__init__(self, parent, *args)
        self.mode=mode
        self.record=record
        self.grdFields=QGridLayout(self)
        self.grdFields.setSpacing(6)
        self.grdFields.setMargin(11)
    
        self.fieldList=[]
        self.fieldTypes={}
        row=0

        for field, fieldDef in record.tableDef.orderedFieldList():
            if fieldDef.dialog: # show in dialog
                self.grdFields.expand(row + 1, 2)
                self.fieldList.append((field, fieldDef))
                self.fieldTypes[field]=fieldDef
        
                if fieldDef.datatype == constants.TEXT: # Multiline
                    if fieldDef.readonly and mode != constants.SEARCH:
                        fld=self.addField(field, guiLabel(self))
                        fld.setAlignment(Qt.AlignLeft or Qt.AlignTop)
                        fld.setFrameShape(guiLabel.Panel)
                        fld.setFrameShadow(guiLabel.Sunken)
                        fld.setFont(font)
                    else:
                        fld=self.addField(field,
                                          guiMultiLineEdit(self))
                        fld.setText(record.getFieldValue(field))
          
                    self.grdFields.addWidget(self.addField("txt"+field,
                                                 guiLabel(fld,
                                                          fieldDef.label,
                                                          self)),
                                             row, 0)
                    self.grdFields.addWidget(fld, row, 1)
          
                elif fieldDef.relation <> None: # Combobox
                    if fieldDef.readonly and mode != constants.SEARCH:
                        fld=self.addField(field, guiLabel(self))
                        fld.setFrameShape(guiLabel.Panel)
                        fld.setFrameShadow(guiLabel.Sunken)
                        fld.setText(record.getFieldValue(record.getDescriptorColumnName(field)))
                        fld.setFont(font)
                    else:
                        fld=self.addField(field, guiComboBox(self))
                        fld.fillComboBox(record, field, self.mode)
          
                    self.grdFields.addWidget(self.addField("txt"+field,
                                                           guiLabel(fld, fieldDef.label, self)),
                                             row, 0)
                    self.grdFields.addWidget(fld, row, 1)
          
                elif fieldDef.datatype == constants.BOOLEAN: # checkbox
                    fld=self.addField(field, guiCheckBox(self, fieldDef.label))
                    if mode == constants.SEARCH:
                        fld.setTristate(True)
                    fld.setChecked(record.getFieldValue(field))
                    if fieldDef.readonly and mode != constants.SEARCH:
                        fld.setEnabled(False)
                      
                    self.grdFields.addWidget(fld, row, 0)
          
                elif fieldDef.datatype == constants.INTEGER: # number
                    if fieldDef.readonly and mode != constants.SEARCH:
                        fld=self.addField(field, guiLabel(self))
                        fld.setFrameShape(guiLabel.Panel)
                        fld.setFrameShadow(guiLabel.Sunken)
                        fld.setFont(font)
                        value = record.getFieldValue(field)
                        if value != None:
                            fld.setText(str(value))
                    else:
                        fld=self.addField(field, guiNumberBox(self))
                        fld.setText(record.getFieldValue(field))
          
                    self.grdFields.addWidget(self.addField("txt"+field,
                                                           guiLabel(fld, fieldDef.label, self)),
                                             row, 0)
                    self.grdFields.addWidget(fld, row, 1)
          
                else:# Lineedit
                    if fieldDef.readonly and mode != constants.SEARCH:
                        fld=self.addField(field, guiLabel(self))
                        fld.setFrameShape(guiLabel.Panel)
                        fld.setFrameShadow(guiLabel.Sunken)
                        fld.setFont(font)
                    else:
                        fld=self.addField(field, guiLineEdit(self))
                        fld.setMaxLength(fieldDef.length)

                    fld.setText(record.getFieldValue(field))
                    self.grdFields.addWidget(self.addField("txt"+field,
                                                           guiLabel(fld, fieldDef.label, self)),
                                             row, 0)
                    self.grdFields.addWidget(fld, row, 1)
                row=row+1


    def getField(self, fieldname):
        """
        Returns the widget with fieldname
        """
        return getattr(self, fieldname)

    def addField(self, fieldname, widget):
        setattr(self, fieldname, widget)
        return widget

    def setFieldValue(self, field, value):
        if hasattr(self, field):
            fld=self.getField(field)
            if isinstance(fld, guiLineEdit) or isinstance(fld,guiMultiLineEdit):
                fld.setText(unicode(value))
            elif isinstance(fld, guiCheckBox):
                fld.setChecked(value)
            elif isinstance(fld,guiComboBox):
                try: # might be not in combo-list
                    fld.setCurrentItem(value)
                except KeyError:
                    QMessageBox.warning("Kura internal error"
                                        , "Value does not exist:" + value + " for field " + field)

    def getFieldText(self, field):
        if hasattr(self, field):
            fld=self.getField(field)
            if (isinstance(fld, guiLineEdit) 
                or isinstance(fld, guiMultiLineEdit) 
                or isinstance(fld, guiNumberBox)
                or isinstance(fld, guiLabel)):
                return unicode(fld.text())
            elif isinstance(fld,guiCheckBox):
                return fld.isChecked()
            elif isinstance(fld,guiComboBox):
                return fld.currentText()
            else:
                raise FieldError("No supported widget for %s" % field)
        else:
            raise FieldError(field)

    def getFieldValue(self, field):
        if hasattr(self, field):
            fld=self.getField(field)
            if (isinstance(fld, guiLineEdit) 
                or isinstance(fld, guiMultiLineEdit) 
                or isinstance(fld, guiNumberBox)
                or isinstance(fld, guiLabel)):
                return fld.text()
            elif isinstance(fld, guiCheckBox):
                return fld.isChecked()
            elif isinstance(fld,guiComboBox):
                return fld.currentKey()
            else:
                raise FieldError("No supported widget for %s" % field)
        else:
            raise FieldError(field)
        
    def refreshComboBoxes(self):
        for field, fieldDef in self.record.tableDef.orderedFieldList():
            fld=self.getField(field)
            if isinstance(fld,guiComboBox):
                fld.clear()
                fld.fillComboBox(self.record, field, self.mode)

__copyright__="""
    copyright            : (C) 2002 by Boudewijn Rempt
                           see copyright notice for license
    email                : boud@valdyas.org
"""

__revision__="""$Revision: 1.10 $"""[11:-2]
