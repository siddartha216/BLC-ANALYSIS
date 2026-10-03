import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ============================================================
# 1. LOAD DATASET
# ============================================================

file_path = "BLC-10.csv"

df = pd.read_csv(file_path)

print("==========================================")
print("DATASET LOADED")
print("==========================================")
print(f"Total records: {len(df)}")


# ============================================================
# 2. CLEAN CATEGORY
# ============================================================

df["Category"] = (
    df["Category"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)


# ============================================================
# 3. STANDARD CATEGORY MAPPING
# ============================================================

def map_to_standard_category(cat):

    cat_lower = str(cat).lower().strip()

    if "coaching" in cat_lower or "caoching" in cat_lower:
        return "Coaching Center"

    if "tutoring" in cat_lower or "tuition" in cat_lower:
        return "Academic Tuition"

    if (
        "training" in cat_lower
        or "education" in cat_lower
        or "educational" in cat_lower
        or "institute" in cat_lower
        or "university" in cat_lower
        or "school" in cat_lower
        or "computer center" in cat_lower
        or "vocational" in cat_lower
    ):
        return "Training Center"

    if "dermatologist" in cat_lower or "skin" in cat_lower:
        return "Dermatologist"

    if "dental" in cat_lower or "dentist" in cat_lower:
        return "Dental Clinic"

    if "physio" in cat_lower:
        return "Physiotherapy Clinic"

    if "pharmacy" in cat_lower:
        return "Pharmacy"

    if "restaurant" in cat_lower or "food" in cat_lower:
        return "Restaurant"

    if "supermarket" in cat_lower:
        return "Supermarket"

    if "bakery" in cat_lower:
        return "Bakery"

    if (
        "salon" in cat_lower
        or "spa" in cat_lower
        or "gym" in cat_lower
    ):
        return "Salon"

    if "grocery" in cat_lower:
        return "Grocery Store"

    if "dairy" in cat_lower:
        return "Dairy Shop"

    # Medical / clinical categories
    if any(
        keyword in cat_lower
        for keyword in [
            "medical",
            "clinic",
            "hospital",
            "doctor",
            "homeopath",
            "health",
            "surgeon",
            "pediatrician",
            "practitioner",
            "care",
            "maternity",
            "nursing",
            "acupuncture",
            "ayurvedic",
            "holistic",
            "orthopaedic",
            "orthopedic"
        ]
    ):
        return "Physiotherapy Clinic"

    return "Training Center"


df["Standard_Category"] = df["Category"].apply(
    map_to_standard_category
)

print("Category standardization completed.")


# ============================================================
# 4. CATEGORY RANKS
# ============================================================

india_ranks = {
    "Training Center": 1,
    "Coaching Center": 2,
    "Dermatologist": 3,
    "Dental Clinic": 4,
    "Physiotherapy Clinic": 5,
    "Restaurant": 6,
    "Supermarket": 7,
    "Academic Tuition": 8,
    "Bakery": 9,
    "Salon": 10,
    "Pharmacy": 11,
    "Grocery Store": 12,
    "Dairy Shop": 13
}


foreign_ranks = {
    "Dental Clinic": 1,
    "Dermatologist": 2,
    "Physiotherapy Clinic": 3,
    "Training Center": 4,
    "Salon": 5,
    "Restaurant": 6,
    "Bakery": 7,
    "Academic Tuition": 8,
    "Coaching Center": 9,
    "Pharmacy": 10,
    "Supermarket": 11,
    "Grocery Store": 12,
    "Dairy Shop": 13
}


# ============================================================
# 5. ASSIGN CATEGORY PROBABILITY
# ============================================================

def assign_probability_and_rank(row):

    country = str(row["Country"]).strip().lower()

    category = row["Standard_Category"]

    if "india" in country:

        rank = india_ranks.get(category, 13)

    else:

        rank = foreign_ranks.get(category, 13)


    # Category probability
    if rank <= 5:

        probability = 0.85

    elif rank <= 10:

        probability = 0.55

    else:

        probability = 0.15


    return pd.Series(
        [probability, rank]
    )


df[
    [
        "Conversion_Probability",
        "Rank"
    ]
] = df.apply(
    assign_probability_and_rank,
    axis=1
)


# ============================================================
# 6. CREATE ADDITIONAL FEATURES
# ============================================================

df["Company_Name_Length"] = (
    df["Company"]
    .astype(str)
    .str.len()
)

df["Company_Word_Count"] = (
    df["Company"]
    .astype(str)
    .str.split()
    .str.len()
)


category_counts = (
    df["Standard_Category"]
    .value_counts()
    .to_dict()
)

df["Category_Frequency"] = (
    df["Standard_Category"]
    .map(category_counts)
)


city_counts = (
    df["City"]
    .value_counts()
    .to_dict()
)

df["City_Frequency"] = (
    df["City"]
    .map(city_counts)
)


# ============================================================
# 7. ENCODE CITY
# ============================================================

le_city = LabelEncoder()

df["City_Encoded"] = le_city.fit_transform(
    df["City"].astype(str)
)


# ============================================================
# 8. ENCODE CATEGORY
# ============================================================

le_category = LabelEncoder()

df["Category_Encoded"] = (
    le_category.fit_transform(
        df["Standard_Category"].astype(str)
    )
)


# ============================================================
# 9. FEATURES
# ============================================================

feature_names = [
    "Company_Name_Length",
    "Company_Word_Count",
    "Category_Frequency",
    "City_Frequency",
    "City_Encoded",
    "Category_Encoded"
]

X = df[feature_names]

y = df["Conversion_Probability"]


# ============================================================
# 10. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ============================================================
# 11. RANDOM FOREST MODEL
# ============================================================

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_model.fit(
    X_train,
    y_train
)


print("\n==========================================")
print("MODEL TRAINING")
print("==========================================")

print(
    f"Training R² Score: "
    f"{rf_model.score(X_train, y_train):.4f}"
)

print(
    f"Testing R² Score: "
    f"{rf_model.score(X_test, y_test):.4f}"
)


# ============================================================
# 12. PREDICT PROBABILITY
# ============================================================

df["Predicted_Probability"] = (
    rf_model.predict(X)
)


# ============================================================
# 13. ASSIGN HIGH / MEDIUM / LOW
# ============================================================

def assign_priority(probability):

    if probability >= 0.70:

        return "High"

    elif probability >= 0.40:

        return "Medium"

    else:

        return "Low"


df["Priority"] = (
    df["Predicted_Probability"]
    .apply(assign_priority)
)


# ============================================================
# 14. SORT DATA
# ============================================================

df_sorted = df.sort_values(
    by=[
        "Predicted_Probability",
        "Rank"
    ],
    ascending=[
        False,
        True
    ]
).reset_index(drop=True)


# ============================================================
# 15. FINAL COLUMNS
# ============================================================

columns_to_export = [
    "S.No",
    "Country",
    "City",
    "Company",
    "CONTACT",
    "Google Map",
    "Category",
    "Standard_Category",
    "Predicted_Probability",
    "Priority"
]


# ============================================================
# 16. CREATE HIGH / MEDIUM / LOW DATAFRAMES
# ============================================================

high_priority = df_sorted[
    df_sorted["Priority"] == "High"
][columns_to_export].copy()


medium_priority = df_sorted[
    df_sorted["Priority"] == "Medium"
][columns_to_export].copy()


low_priority = df_sorted[
    df_sorted["Priority"] == "Low"
][columns_to_export].copy()


# ============================================================
# 17. OUTPUT FILE
# ============================================================

output_filename = "Cat_Probability.xlsx"


# ============================================================
# 18. WRITE EXCEL
# ============================================================

with pd.ExcelWriter(
    output_filename,
    engine="openpyxl"
) as writer:

    high_priority.to_excel(
        writer,
        sheet_name="High",
        index=False
    )

    medium_priority.to_excel(
        writer,
        sheet_name="Medium",
        index=False
    )

    low_priority.to_excel(
        writer,
        sheet_name="Low",
        index=False
    )


# ============================================================
# 19. FORMAT EXCEL
# ============================================================

wb = load_workbook(
    output_filename
)


for ws in wb.worksheets:

    probability_column = None

    contact_column = None


    # Find columns
    for cell in ws[1]:

        if cell.value == "Predicted_Probability":

            probability_column = cell.column

        if cell.value == "CONTACT":

            contact_column = cell.column


    # --------------------------------------------------------
    # Probability formatting
    # --------------------------------------------------------

    if probability_column is not None:

        for row in range(
            2,
            ws.max_row + 1
        ):

            cell = ws.cell(
                row=row,
                column=probability_column
            )

            cell.number_format = "0.00%"


    # --------------------------------------------------------
    # CONTACT as text
    # --------------------------------------------------------

    if contact_column is not None:

        for row in range(
            2,
            ws.max_row + 1
        ):

            cell = ws.cell(
                row=row,
                column=contact_column
            )

            cell.number_format = "@"


    # --------------------------------------------------------
    # Header formatting
    # --------------------------------------------------------

    for cell in ws[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="595959"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )


    # --------------------------------------------------------
    # Column width
    # --------------------------------------------------------

    for column_cells in ws.columns:

        max_length = 0

        column_letter = (
            column_cells[0].column_letter
        )

        for cell in column_cells:

            try:

                cell_length = len(
                    str(cell.value)
                )

                if cell_length > max_length:

                    max_length = cell_length

            except:

                pass


        ws.column_dimensions[
            column_letter
        ].width = min(
            max_length + 2,
            50
        )


# ============================================================
# 20. SAVE FILE
# ============================================================

wb.save(
    output_filename
)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print("\n==========================================")
print("CATEGORY PRIORITY MODEL COMPLETED")
print("==========================================")

print(
    f"Output file: {output_filename}"
)

print(
    f"\nHigh Priority   : {len(high_priority)}"
)

print(
    f"Medium Priority : {len(medium_priority)}"
)

print(
    f"Low Priority    : {len(low_priority)}"
)

print(
    f"Total            : "
    f"{len(high_priority) + len(medium_priority) + len(low_priority)}"
)

print("\nSheets created:")

print("1. High")
print("2. Medium")
print("3. Low")

print(
    "\nEach sheet contains businesses from ALL categories."
)

print(
    "Category is retained in the Category column."
)

print(
    "\nFile created successfully:"
)

print(
    output_filename
)