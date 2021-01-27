import xml.sax
from pycfdi_transform.sax.base33_handler import Base33Handler


class CFDI33Handler (xml.sax.ContentHandler, Base33Handler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        Base33Handler.__init__(self)
        self._start_concept = False
        self._start_complement = False
        self._complement_profundity = 0
        self._start_addenda = False
        self._addenda_profundity = 0

    def startElement(self, tag, attrs):
        if (tag == 'cfdi:Comprobante'):
            Base33Handler.transform_comprobante(self, tag, attrs)
        elif (tag == 'cfdi:Emisor'):
            Base33Handler.transform_emisor(self, tag, attrs)
        elif (tag == 'cfdi:Receptor'):
            Base33Handler.transform_receptor(self, tag, attrs)
        elif (tag == 'cfdi:Concepto'):
            self._start_concept = True
            self.__transform_conceptos(tag, attrs)
        elif (tag == 'cfdi:Impuestos' and self._start_concept == False):
             self.__transform_impuestos(tag, attrs)
        elif (tag == 'cfdi:Traslado' and self._start_concept == False):
            self.__transform_impuestos_traslados(tag, attrs)
        elif (tag == 'cfdi:Retencion' and self._start_concept == False):
            self.__transform_impuestos_retenciones(tag, attrs)
        elif (tag == 'cfdi:Complemento'):
            self._start_complement = True
        elif (tag == 'tfd:TimbreFiscalDigital'):
            self._complement_profundity += 1
            Base33Handler.transform_tfd(self, tag, attrs)
        elif (tag == 'implocal:ImpuestosLocales'):
            self._complement_profundity += 1
            self.__transform_imploc(tag, attrs)
        elif (self._start_complement):
            self._complement_profundity += 1
        elif (tag == 'cfdi:Addenda'):
            self._start_addenda = True
        elif (self._start_addenda):
            self._addenda_profundity += 1
            
    def endElement(self, tag):
        if (tag == 'cfdi:Concepto'):
            self._start_concept = False
        elif (tag == 'cfdi:Complemento'):
            self._start_complement = False
        elif (self._start_complement):
            self._complement_profundity -= 1
            if(self._complement_profundity == 0):
                self.__transform_complementos(tag)
        elif (tag == 'cfdi:Addenda'):
            self._start_addenda = False
        elif (self._start_addenda):
            self._addenda_profundity -= 1
            if(self._addenda_profundity == 0):
                self.__transform_addenda(tag)
            
    
    def __transform_conceptos(self, tag, attrs):
        if ('ClaveProdServ' in attrs):
            self._clave_prod_serv = Base33Handler.concatenate(self, self._clave_prod_serv, attrs['ClaveProdServ'])

    def __transform_impuestos(self, tag, attrs):
        if ('TotalImpuestosTrasladados' in attrs):
            self._total_impuestos_traslado = Base33Handler.sum(self, 
                self._total_impuestos_traslado, attrs['TotalImpuestosTrasladados'])
        if ('TotalImpuestosRetenidos' in attrs):
            self._total_impuestos_retenidos = Base33Handler.sum(self,
                self._total_impuestos_retenidos, attrs['TotalImpuestosRetenidos'])
        
    def __transform_impuestos_traslados(self, tag, attrs):
        if ('Impuesto' in attrs and 'Importe' in attrs):
            if (attrs['Impuesto'] == '002'):
                self._iva_traslado = Base33Handler.sum(self, 
                    self._iva_traslado, attrs['Importe'])
            elif (attrs['Impuesto'] == '003'):
                self._ieps_traslado = Base33Handler.sum(self, 
                    self._ieps_traslado, attrs['Importe'])
    
    def __transform_impuestos_retenciones(self, tag, attrs):
        if ('Impuesto' in attrs and 'Importe' in attrs):
            if(attrs['Impuesto'] == '001'):
                self._isr_retenido = Base33Handler.sum(self, 
                    self._isr_retenido, attrs['Importe'])
            elif (attrs['Impuesto'] == '002'):
                self._iva_retenido = Base33Handler.sum(self, 
                    self._iva_retenido, attrs['Importe'])
            elif (attrs['Impuesto'] == '003'):
                self._ieps_retenido = Base33Handler.sum(self,
                    self._ieps_retenido, attrs['Importe'])

    def __transform_complementos(self, tag):
        complement_name = tag
        if (':' in tag):
            complement_name = tag[tag.rindex(':') + 1:]
        self._complementos = Base33Handler.concatenate(self, self._complementos, complement_name)

    def __transform_addenda(self, tag):
        addenda_name = tag
        if (':' in tag):
            addenda_name = tag[tag.rindex(':') + 1:]
        self._addendas = Base33Handler.concatenate(self, self._addendas, addenda_name)

    def __transform_imploc(self, tag, attrs):
        if ('TotaldeTraslados' in attrs):
            self._total_traslados_impuestos_locales = Base33Handler.sum(self, 
                self._total_traslados_impuestos_locales, attrs['TotaldeTraslados'])
        if ('TotaldeRetenciones' in attrs):
            self._total_retenciones_impuestos_locales = Base33Handler.sum(self, 
                self._total_retenciones_impuestos_locales , attrs['TotaldeRetenciones'])
    
    def get_addendas(self) -> str:
        return self._addendas

    
