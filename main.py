# main.py
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np
from textwrap import wrap


def hello(): # Fonction de test
    print("Hello, world!")

# Données stratigraphiques
System_Period = {
    "System/Period": [
        "Quaternary", "Neogene", "Paleogene", "Cretaceous", "Jurassic",
        "Triassic", "Permian", "Carboniferous", "Devonian", "Silurian",
        "Ordovician", "Cambrian"
    ],
    "ages": [
        0, 2.58, 23.04, 66, 143.1,
        201.4, 251.902, 298.9, 358.86, 419.62,
        443.1, 486.85, 538.8
    ],
    "fill_color": [
        "#fff79a", "#ffdd2b", "#f9a86f", "#85c86f",
        "#00b9e7", "#8e52a1", "#e76549", "#68aeb1",
        "#ce9c5a", "#b2ddca", "#00a78e", "#8aaa78"
    ],
    "font_color": [
        "k", "k", "k", "k", "w", "w", "k", "w", "k", "k", "w", "w"
    ]
}

# Data input with validation
def import_data(data_path):
    
    """
    Reads a CSV file, validates its contents, and checks data consistency.

    Args:
        data_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The validated DataFrame if validation succeeds.

    Raises:
        ValueError: If the validation fails or the file has issues.
    """
    try:
        # Charger les données
        df = pd.read_csv(data_path, sep=';')

        # Vérification des colonnes nécessaires
        required_columns = ['Name', 'Type', 'Top', 'Thickness', 'Deposed', 'Eroded', 'Age at top']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Validation failed: Missing required columns in the dataset. Required columns are: Name, Type, Top, Thickness, Deposed, Eroded, Age at top. Please check headers of the CSV file.")

        # Extraction des données
        Deposed = np.array(df['Deposed'], dtype=int)
        Eroded = np.array(df['Eroded'], dtype=int)
        Thickness = np.array(df['Thickness'], dtype=int)
        Topes = np.array(df['Top'], dtype=int)

        # Validation des données
        if not (Deposed.sum() - Eroded.sum() == Thickness.sum()):
            raise ValueError(
                f"Validation failed: Deposits, Erosions, and Thickness are inconsistent. "
                f"Please check the data consistency."
            )
        
        if max(Topes) != Thickness.sum():
            raise ValueError(
                f"Validation failed: The total depth should equal the sum of thickness. "
                f"Please check the 'Top' values."
            )
        
        # Retourner le DataFrame validé
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {data_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("Error: The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error: The file could not be parsed as a CSV.")
    except pd.errors.DtypeWarning:
        raise ValueError("Warning: Data type conversion warning.")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")

def run(df):
        Bilan = df['Deposed']-df['Eroded'] # Calcul du bilan sédimentaire pour chaque periode. si Bilan positif, la base de couche s'enfouis, si négatif, la base de couche s'élève.
        # Calcul de la courbe de base (la base de toute la section étudiée)
        Base_curve=(Bilan)[::-1].cumsum()[::-1]
        Curve = pd.DataFrame()
        Curve['Ages']=df['Age at top']
        Curve['Base_curve']=Base_curve
        # Calcul d'autres courbes (les bases d'autres couches)
        points=np.zeros((len(Bilan),len(Bilan)))
        points[:,0]=Base_curve
        mrg = np.array(Bilan[:-1])[::-1]
        for i in range(0,len(Base_curve)):
            for j in range(1,len(mrg)):
                points[i,j]=points[i,j-1]-mrg[j-1]
        points_df = pd.DataFrame(points)
        for i in range(2,len(points_df)):
            for j in range(1,len(points_df.columns)):
                if  j+1 >= len(points_df) - i:
                    points_df.loc[i,j]= 0
        # Dictionary mapping old column names to new ones
        Types = np.array(df['Type'])[::-1]
        Types = dict(zip(points_df.columns, Types))
        points_df.rename(columns=Types, inplace=True)
        points_df = points_df.drop(columns='D')
        points_df['A'] = df['Age at top']
        return points_df

# Fonction pour tronquer le texte
def truncate_text(text, start, end, age_max, fig_width):
    rectangle_width = (end - start) / age_max * fig_width * 100
    char_width = 8
    max_chars = int(rectangle_width / char_width)
    if max_chars < 1:
        return ''
    if max_chars == 1:
        return text[:max_chars]
    if len(text) > max_chars:
        return text[:max_chars] + '-'
    return text

# Fonction pour configurer les axes du graphique supérieur
def stratigraphic_chart(ax, ages, fig_width, age_max):
    texts = System_Period["System/Period"]
    colors = System_Period["fill_color"]
    font_color = System_Period["font_color"]
    # Dessiner les rectangles et ajouter le texte
    for i in range(len(texts)):
        if i + 1 >= len(ages):  # Éviter les erreurs d'indice
            break
        start, end = ages[i], ages[i + 1]
        if (start + end) / 2 > age_max:  # Ignorer les rectangles en dehors de l'axe
            continue
        ax.fill_between([start, end], 0, 1, color=colors[i], edgecolor='black', linewidth=0.5)
        truncated_text = truncate_text(texts[i], start, end, age_max, fig_width)
        ax.text((start + end) / 2, 0.5, truncated_text, ha='center', va='center', 
                     color=font_color[i])      
    ax.set_xlim(0, age_max)
    ax.set_ylim(0, 1)
    ax.tick_params(axis='y', which='both', length=0, labelleft=False, labelbottom=False)
    ax.tick_params(axis='x', top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xlabel('Time (My)', fontsize=9, labelpad=10, fontname='Times New Roman')
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.tick_params(axis='x', top=True, bottom=False, which='minor', length=2, color='r')
    ax.invert_xaxis()
    
# Fonction pour configurer les axes du graphique inférieur
def burial_history_curves(ax, age_max, depth_max, points_df):
        # Tracer les courbes d'enfouissement
    points = points_df.drop(columns='A')
    points = points.values
    for i in range(0,len(points.T)):
        ax.plot(points_df['A'], points.T[i],color='black',linewidth=0.5)
    ax.set_xlim(0, age_max)
    ax.set_ylim(0, depth_max)
    ax.invert_yaxis()
    ax.invert_xaxis()
    ax.tick_params(axis='x', which='both', length=0, labelleft=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, labelbottom=False, labelright=False)
    ax.yaxis.set_minor_locator(MultipleLocator(50))
    ax.tick_params(axis='y', left=True, right=False, which='minor', length=2, color='r')
    ax.set_ylabel('Depth (m)', fontsize=9, labelpad=5, fontname='Times New Roman')
    ax.yaxis.set_label_position('left')

def stratigraphic_log(ax, depth_max, df):
    log_formation = df[df['Type'].isin(['N', 'B'])]
    ax.hlines(df['Top'], 0, 1, color='black', linewidth=0.5)
    formations = log_formation['Name']
    text_y_coord = log_formation['Top']
    for i in range(len(formations) - 1):
        y_position = (text_y_coord.iloc[i] + text_y_coord.iloc[i + 1]) / 2  # Moyenne des positions Y
        width_in_points = 11  # Conversion cm → points
        # Découper le texte avec `textwrap`
        wrapped_text = "\n".join(wrap(formations.iloc[i], width=int(width_in_points)))  # Facteur 8 pour approximer la largeur des caractères        
        ax.text(0.5, y_position, wrapped_text, ha='center', va='center', color='black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, depth_max)
    ax.invert_yaxis()
    ax.tick_params(axis='x', which='both', top=False, bottom=False, labeltop=False, labelbottom=False)
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelbottom=False, labelright=False)

# Fonction principale pour tracer les courbes d'enfouissemnt
def BH(df, axes, fig_width):
    points_df = run(df) 
    depth_max = max(points_df['B'])  # Trouver la profondeur maximum
    age_max = max(points_df['A'])  # Trouver l'âge maximum
    # Extraire les ages du système/période
    ages = System_Period["ages"]
    # Mettre à jour age_max en fonction de la valeur dans ages
    for i in range(1, len(ages)):
        if ages[i - 1] < age_max < ages[i]:
            age_max = ages[i]
            break
    # Afficher la charte stratigraphique
    stratigraphic_chart(axes[0,0], ages, fig_width, age_max)
    # Désactiver l'axes[0,1]
    axes[0,1].axis('off')
    # Tracer les courbes d'enfouissement
    burial_history_curves(axes[1,0], age_max, depth_max, points_df)
    # Tracer le log stratigraphique
    stratigraphic_log(axes[1,1], depth_max, df)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    if isinstance(axes, np.ndarray):
        for ax in axes.flat:  # Utilisez flat pour parcourir même les tableaux 2D
            ax.tick_params(labelsize=8)  # Taille de la police des ticks
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontname("Times New Roman")
    else:  # Si axes est un seul objet
        axes.tick_params(labelsize=8)
        for label in axes.get_xticklabels() + axes.get_yticklabels():
            label.set_fontname("Times New Roman")

# Fonction principale pour afficher les courbes d'enfouissemnt
def plot(df):
    # Création de la figure et des axes
    fig_width = 16 / 2.54
    fig_height = 11 / 2.54
    fig, axes = plt.subplots(2, 2, figsize=(fig_width, fig_height), gridspec_kw={'height_ratios': [1, 20], 'width_ratios': [15, 2]})
    # Mise à jour des paramètres de police
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': 'Times New Roman',
        'font.size': 8
    })
    BH(df, axes, fig_width)
    plt.close()
    return fig


def save_fig(fig, save_path):
    fig.savefig(save_path, dpi=300, bbox_inches='tight')