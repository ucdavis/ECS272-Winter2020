feats_textual = ['Name']
# TODO figure out more complex mapping for types with domain knowledge of strengths
feats_categorical = ['Type_1', 'Type_2', 'Color', 'Egg_Group_1', 'Egg_Group_2', 'Body_Style']
feats_numeric = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def',
                 'Speed', 'Pr_Male', 'Height_m', 'Weight_kg', 'Catch_Rate']
feats_ordinal = ['Generation']
feats_bool = ['isLegendary', 'hasGender', 'hasMegaEvolution']

# Manually the pokemon type to correspond roughly to their canonical color
type_colors = {
    "Grass": "lightgreen",
    "Fire": "red",
    "Water": "darkblue",
    "Bug": "darkgreen",
    "Normal": "darkcyan",
    "Poison": "purple",
    "Electric": "yellow",
    "Ground": "burlywood",
    "Fairy": "pink",
    "Fighting": "orange",
    "Psychic": "pink",
    "Rock": "brown",
    "Ghost": "blue",
    "Ice": "lightblue",
    "Dragon": "cyan",
    "Dark": "black",
    "Steel": "darkgrey",
    "Flying": "turquoise",
    "nan": "ivory"
}

# https://bulbapedia.bulbagarden.net/wiki/Egg_Group
egg_group_colors = {
    "Dragon": type_colors['Dragon'],
    "nan": type_colors['nan'],
    "Water_3": "darkblue",
    "Water_2": "blue",
    "Water_1": "lightblue",
    "Ditto": "fuchsia",
    "Human-Like": "tan",
    "Mineral": "brown",
    "Fairy": "pink",
    "Monster": "red",
    "Undiscovered": "black",
    "Bug": "yellow",
    "Grass": "green",
    "Flying": "purple",
    "Field": "orange",
    "Amorphous": "grey"
}

# A mapping between a column name to dict that maps from feature value to display
# color.
feat_colors = {
    "Type_1": type_colors,
    "Type_2": type_colors,
    # For color values we can directly map to itself
    "Color": {
        value: value.lower()
        for value in ['Green', 'Red', 'Blue', 'White',
                      'Brown', 'Yellow', 'Purple', 'Pink', 'Grey', 'Black']
    },
    "Egg_Group_1": egg_group_colors,
    "Egg_Group_2": egg_group_colors,
    "Body_Style": {
        "with_fins": "blue",
        "two_wings": "pink",
        "multiple_bodies": "yellow",
        "head_only": "red",
        "head_legs": "orange",
        "four_wings": "purple",
        "quadruped": "green",
        "head_arms": "tan",
        "head_base": "beige",
        "bipedal_tailed": "navy",
        "several_limbs": "cyan",
        "insectoid": "brown",
        "serpentine_body": "darkgreen",
        "bipedal_tailless": "teal"

    }
}

bool_colors = {
    True: "green",
    False: "red"
}


feats_all = feats_numeric + feats_bool + feats_categorical + feats_ordinal
