from flask import Flask
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Configuration des graphiques
plt.style.use('default')
sns.set_palette("husl")


app = Flask(__name__)


# Date de référence pour le calcul de la récence
reference_date = datetime(2024, 1, 1)

# Génération de données de transactions
np.random.seed(42)
n_customers = 1000
n_transactions = 5000

# Génération des données clients
customer_ids = np.random.randint(1, n_customers + 1, n_transactions)
transaction_dates = pd.date_range(
    start=datetime(2022, 1, 1),
    end=datetime(2023, 12, 31),
    freq='D'
)
transaction_dates = np.random.choice(transaction_dates, n_transactions)

# Montants des transactions (distribution log-normale)
amounts = np.random.lognormal(mean=3, sigma=1, size=n_transactions)

# Création du DataFrame
df_transactions = pd.DataFrame({
    'customer_id': customer_ids,
    'transaction_date': transaction_dates,
    'amount': amounts
})

print(f"Dataset généré: {len(df_transactions)} transactions pour {len(df_transactions['customer_id'].unique())} clients")
print(f"Période: {df_transactions['transaction_date'].min()} à {df_transactions['transaction_date'].max()}")
print(f"Montant moyen: {df_transactions['amount'].mean():.2f}€")
print("\nAperçu des données:")
print(df_transactions.head())


@app.route('/')
def hello_world():
    return 'Hello, World!'
