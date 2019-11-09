
def checkIfDiff(x):
        if(x[-1] == "*"):
            return 1
        else:
            return 0

class PlayerProfile():
    
    handicap = 999
    matricula = 0
    validez = ''
    nombre = 'NAN'
    
    def getDifferentials(self, df):
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header
        df['is_dif'] = df['Diferenciales'].apply(lambda x: checkIfDiff(x))
        df['Diferenciales'] = (df['Diferenciales'].str.strip('*'))
        df['Diferenciales'] = df['Diferenciales'].apply(lambda x: float(x.replace(",", ".")))
        df['matricula'] = self.matricula
        self.diferenciales = df
    
    def getOverallStats(self, df):
        results = []
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header

        handicap_raw = df.loc[1,:].values[0]
        self.handicap = int(handicap_raw[-(len(handicap_raw)-10):])

        matricula_raw = df.loc[1,:].values[1]
        self.matricula = int(matricula_raw[-(len(matricula_raw)-16):])

        valido_raw = df.loc[1,:].values[2]
        self.validez = valido_raw[-(len(valido_raw)-15):]
    
    def __init__(self, data):
        #Saco las estadisticas generales
        try:
            df = pd.read_html(data, flavor="lxml", decimal=",", thousands=None)[0]
            self.getOverallStats(df)

            #Saco los diferenciales del jugador
            df = pd.read_html(data, flavor="lxml", decimal=',', thousands=None)[2]
            self.getDifferentials(df)
            
            df_header = pd.read_html(response.text, flavor="lxml", decimal=',', thousands=None)[0].iloc[0]
            self.nombre = df_header[0][-(len(df_header[0])-19):]
        except:
            pass

class PlayerSet():
    players = []
    
    def __init__(self):
        self.players = []
        pass
    
    def newPlayer(self, PlayerProfile):
        self.players.append(PlayerProfile)