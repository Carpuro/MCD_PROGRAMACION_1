import pandas as pd
import matplotlib.pyplot as plt

# 1. Load CSV file
df = pd.read_csv(
    r"C:\Users\carlo\OneDrive\Documentos\Maestría en Ciencia de los Datos\Semestre 1\PROGRAMACIÓN 1\Sesion 1 (12-08-2025)\categoria_de_corredores.csv"
)
# 2. Check DataFrame info
df.info()
df.head()

# 3. Create a histogram of one column
plt.figure(1)
plt.hist(df["Tiempo"], bins=15, color="yellow", edgecolor="black")
plt.title("Histograma de Tiempo")
plt.savefig("Histograma.jpg")
plt.show()