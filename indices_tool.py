from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsRasterLayer


class SATool:
    def __init__(
        self, index_name, red_band, nir_band, output, swir_band,      
    ):
        self.index = index_name
        self.red = red_band
        self.nir = nir_band
        self.swir = swir_band

        self.output = output

    def calc_ndvi(self):
        r = QgsRasterCalculatorEntry()
        r.ref = self.red.name() + '@1'
        r.raster = self.red
        r.bandNumber = 1

        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@2'
        ir.raster = self.nir
        ir.bandNumber = 1

        entries = list()
        entries.append(r)
        entries.append(ir)

        expression = '({0} - {1}) / ({0} + {1})'.format(ir.ref, r.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.red.extent(), self.red.width(), self.red.height(),
            entries
        )
        calc.processCalculation()

    def calc_rvi(self):
        r = QgsRasterCalculatorEntry()
        r.ref = self.red.name() + '@1'
        r.raster = self.red
        r.bandNumber = 1

        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@2'
        ir.raster = self.nir
        ir.bandNumber = 1

        entries = list()
        entries.append(r)
        entries.append(ir)

        expression =  '{0} / {1}'.format(ir.ref, r.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.red.extent(), self.red.width(), self.red.height(),
            entries
        )
        calc.processCalculation()
        
    
    def calc_dvi(self):
        r = QgsRasterCalculatorEntry()
        r.ref = self.red.name() + '@1'
        r.raster = self.red
        r.bandNumber = 1

        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@2'
        ir.raster = self.nir
        ir.bandNumber = 1

        entries = list()
        entries.append(r)
        entries.append(ir)

        expression =  '{0} - {1}'.format(ir.ref, r.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.red.extent(), self.red.width(), self.red.height(),
            entries
        )
        calc.processCalculation()
            
    
    def calc_ipvi(self):
        r = QgsRasterCalculatorEntry()
        r.ref = self.red.name() + '@1'
        r.raster = self.red
        r.bandNumber = 1

        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@2'
        ir.raster = self.nir
        ir.bandNumber = 1

        entries = list()
        entries.append(r)
        entries.append(ir)

        expression =  '{0}/({0} + {1})'.format(ir.ref, r.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.red.extent(), self.red.width(), self.red.height(),
            entries
        )
        calc.processCalculation()
            
    def calc_ndwi(self):
        
        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@1'
        ir.raster = self.nir
        ir.bandNumber = 1

        swir = QgsRasterCalculatorEntry()
        swir.ref = self.swir.name() + '@2'
        swir.raster = self.swir
        swir.bandNumber = 1


        entries = list()
        entries.append(ir)
        entries.append(swir)

        expression =  '({0} - {1})/({0} + {1})'.format(ir.ref, swir.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.nir.extent(), self.nir.width(), self.nir.height(),
            entries
        )
        calc.processCalculation()
     
    def calc_ndbi(self):
        
        ir = QgsRasterCalculatorEntry()
        ir.ref = self.nir.name() + '@1'
        ir.raster = self.nir
        ir.bandNumber = 1

        swir = QgsRasterCalculatorEntry()
        swir.ref = self.swir.name() + '@2'
        swir.raster = self.swir
        swir.bandNumber = 1


        entries = list()
        entries.append(ir)
        entries.append(swir)

        expression =  '({0} - {1})/({0} + {1})'.format(swir.ref, ir.ref)

        calc = QgsRasterCalculator(
            expression,
            self.output, "GTiff",
            self.nir.extent(), self.nir.width(), self.nir.height(),
            entries
        )
        calc.processCalculation()
   
 
