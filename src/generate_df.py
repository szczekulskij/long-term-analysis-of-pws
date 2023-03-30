import pandas as pd

def format_df(df):
    df.rename(columns = {
        "nazwisko" : "surname",
        "czas " : "time",
        "total clearence effect wzgledem poczatku" : "total_GCE",
        "wizyta po ilu zabiegach" : "visit_nr",
        "total clearence pomiedzy wizytami" : "inbetween_GCE",
        "Zmiana powierzchni w %\n(Area change)" : "total_area_change",
        "Zmiana koloru wzgledem poczatku\n(Clearence Effect)" : "total_clearence_effect",
        "Bezwgledna zmiana powierzchni\n(Area change inbetween visits)" : "inbetween_area_change",
        "Clearence effect% między następowymi wizytami\n(Clearence Effect inbetween visits)" : "inbetween_clearence_effect"
        }, inplace = True)
    df.drop(columns = ['date of birth', 'previous treatment', 'uprzednie leczenie info'], inplace= True)
    df = df[["surname", "visit_nr", "time", "total_GCE", "total_area_change", "total_clearence_effect", "inbetween_GCE", "inbetween_area_change", "inbetween_clearence_effect"]]
    # strig spaces:
    def strip_space_robust(cell):
        try : 
            float(cell)
            return cell
        except:
            try:
                str(cell)
                return cell.replace(" ", "")
            except:
                raise Exception("Something went wrong!")
    df = df.applymap(strip_space_robust)
    return df

def fill_surnames(df):
    new_surname = []
    current_surname = ''
    for i in df['surname']:
        if type(i) == str:
            current_surname = i
        new_surname.append(current_surname)
    df['surname'] = new_surname
    return df

def filter_df(df):
    df = df.loc[~df.total_GCE.isin(["brakzdjęcia", "brakdanych"])]
    df = df.loc[~df.total_GCE.isnull()]
    df = df.loc[~df.visit_nr.isin(["niebyłozabiegu", "brakzabiegu"])]
    return df

def get_data_df(type = "total"):
    df = pd.read_excel('/Users/szczekulskij/side_projects/long-term-analysis-of-pws/data/final_version.xlsx', sheet_name="wszystkie dane poprawione") 
    df = format_df(df) # rename columns, drop columns, reorder df
    df = filter_df(df)
    df = fill_surnames(df) # fill in surnames info
    if type == "total":
        df.drop(columns = ["inbetween_GCE", "inbetween_area_change", "inbetween_clearence_effect"], inplace = True)
    elif type == "inbetween":
        df.drop(columns = ["total_GCE", "total_area_change", "total_clearence_effect"], inplace = True)
    else : 
        raise Exception(f"Wrong type passed in!. Type was : {type}. But has to be either 'total' or 'inbetween'")
    for column in df.columns:
        df = df.loc[df[column] != "brak"]
    return df


if __name__ == "__main__":
    df = get_data_df("inbetween")
    print(df.head(50))