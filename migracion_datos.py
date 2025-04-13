import pandas as pd

df_resultado = pd.read_excel('tabla_padres_actualizada.xlsx')
df_resultado.fillna('no dato').to_excel('resultado.xlsx',index=False)
