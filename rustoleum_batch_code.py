import datetime


def convert_batch_to_mfg(batch_codes):
    converted_batch_code = []

    years = ["2020", "2021", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

    years_gen = [year for year in range(datetime.datetime.today().year - 1, 2023)]

    print(years_gen)

    months = ["0" + str(day) if day < 10 else str(day) for day in range(1, 13)]

    check_month = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "O", "N", "D"]

    check_days = ["0" + str(day) if day < 10 else str(day) for day in range(1, 32)]

    for index, batch_code in enumerate(batch_codes):

        stripped_bc = batch_code.strip()
        batch_code = list(stripped_bc)

        if len(batch_code) < 6:
            batch = {
                "batch_code": stripped_bc,
                "mfg": "Batch code should be not less than 6"
            }
            return converted_batch_code.append(batch)
            # YEAR
        try:
            if not batch_code[1].isnumeric() or int(batch_code[1]) > len(years) - 1:
                batch = {
                    "batch_code": stripped_bc,
                    "mfg": "There was an error in batch code year"
                }
                return converted_batch_code.append(batch)

            else:
                try:
                    year = years[int(batch_code[1])]
                except IndexError:
                    batch = {
                        "batch_code": stripped_bc,
                        "mfg": "There was an error in batch code year"
                    }
                    return converted_batch_code.append(batch)

        except IndexError:
            batch = {
                "batch_code": stripped_bc,
                "mfg": "Blank batch code"
            }
            return converted_batch_code.append(batch)


            # MONTH
        try:
            if batch_code[2] not in check_month:
                batch = {
                    "batch_code": stripped_bc,
                    "mfg": "There was an error in batch code month"
                }
                return converted_batch_code.append(batch)

            else:
                if batch_code[2] == "O":
                    batch_code[2] = 10
                elif batch_code[2] == "N":
                    batch_code[2] = 11
                elif batch_code[2] == "D":
                    batch_code[2] = 12
                month = months[int(batch_code[2]) - 1]
        except IndexError:
            batch = {
                "batch_code": stripped_bc,
                "mfg": "Blank batch code"
            }
            return converted_batch_code.append(batch)

            # DAYS
        try:
            day_code = batch_code[3] + batch_code[4]
        except IndexError:
            batch = {
                "batch_code": stripped_bc,
                "mfg": "There was an error in batch code days"
            }
            return converted_batch_code.append(batch)

        if day_code not in check_days:
            batch = {
                "batch_code": stripped_bc,
                "mfg": "There was an error in batch code days"
            }
            return converted_batch_code.append(batch)
        else:
            day = day_code

        mfg_date = year + "-" + month + "-" + day + " 12:01:00"

        try:
            final_date = datetime.datetime.strptime(mfg_date, '%Y-%m-%d %H:%M:%S')

            batch = {
                "batch_code": stripped_bc,
                "mfg": final_date
            }

            converted_batch_code.append(batch)

        except:
            batch = {
                "batch_code": stripped_bc,
                "mfg": final_date
            }

            return converted_batch_code.append(batch)
