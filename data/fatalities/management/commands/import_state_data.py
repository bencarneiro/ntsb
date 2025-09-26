from django.core.management.base import BaseCommand
from fatalities.models import State

state_data = [
    ['Alabama','ALDOT','over five million'],
    ['Alaska','DOT&PF','almost one million'],
    ['Arizona','ADOT','over seven million'],
    ['Arkansas','ARDOT','over three million'],
    ['California','Caltrans','forty million'],
    ['Colorado','CDOT','almost six million'],
    ['Connecticut','CTDOT','over three million'],
    ['Delaware','DelDOT','over one million'],
    ['Florida','FDOT','over twenty million'],
    ['Georgia','GDOT','over ten million'],
    ['Hawaii','HDOT','over a million'],
    ['Idaho','ITD','over two million'],
    ['Illinois','IDOT','over twelve million'],
    ['Indiana','INDOT','almost seven million'],
    ['Iowa','Iowa DOT','over three million'],
    ['Kansas','KDOT','almost three million'],
    ['Kentucky','KYTC','almost five million'],
    ['Louisiana','DOTD','almost five million'],
    ['Maine','MaineDOT','over a million'],
    ['Maryland','MDOT','over six million'],
    ['Massachusetts','MassDOT','over seven million'],
    ['Michigan','MDOT','over ten million'],
    ['Minnesota','MnDOT','over five million'],
    ['Mississippi','MDOT','almost three million'],
    ['Missouri','MoDOT','over six million'],
    ['Montana','MDT','over a million'],
    ['Nebraska','NDOT','over two million'],
    ['Nevada','NDOT','over three million'],
    ['New Hampshire','NHDOT','over a million'],
    ['New Jersey','NJDOT','almost ten million'],
    ['New Mexico','NMDOT','over two million'],
    ['New York','NYSDOT','almost twenty million'],
    ['North Carolina','NCDOT','over ten million'],
    ['North Dakota','NDDOT','almost a million'],
    ['Ohio','OHIODPT','over ten million'],
    ['Oklahoma','ODOT','over four million'],
    ['Oregon','ODOT','over four million'],
    ['Pennsylvania','PennDOT','over thirteen million'],
    ['Rhode Island','RIDOT','over a million'],
    ['South Carolina','SCDOT','over five million'],
    ['South Dakota','SDDOT','almost a million'],
    ['Tennessee','TDOT','over seven million'],
    ['Texas','TxDOT','over thirty million'],
    ['Utah','UDOT','over three million'],
    ['Vermont','VTrans','over six hundred thousand'],
    ['Virginia','VDOT','almost nine million'],
    ['Washington','WSDOT','almost eight million'],
    ['West Virginia','WVDOT','almost two million'],
    ['Wisconsin','WisDOT','almost six million'],
    ['Wyoming','WYDOT','over five hundred thousand'],
]

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for row in state_data:
            state = State.objects.get(name=row[0].upper())
            print(state)
            state.dot_name = row[1]
            state.population_description = row[2]
            state.save()