import datetime


def convert_batch_to_mfg(batch_codes):
    converted_batch_code = []

    print(batch_codes)

    years = ["2020", "2021", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

    # years_gen = [year for year in range(datetime.datetime.today().year - 1, 2023)]
    #
    # print(years_gen)

    months = ["0" + str(day) if day < 10 else str(day) for day in range(1, 13)]

    check_month = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "O", "N", "D"]

    check_days = ["0" + str(day) if day < 10 else str(day) for day in range(1, 32)]

    for index, batch_code in enumerate(batch_codes):

        print(batch_code)

        stripped_bc = batch_code.strip()
        batch_code = list(stripped_bc)

        if len(batch_code) < 6:
            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "Batch code should be not less than 6"
            }
            converted_batch_code.append(batch)
            continue
            # YEAR
        try:
            if not batch_code[1].isnumeric() or int(batch_code[1]) > len(years) - 1:
                batch = {
                    "index": index + 1,
                    "batch_code": stripped_bc,
                    "mfg": "There was an error in batch code year"
                }
                converted_batch_code.append(batch)
                continue

            else:
                try:
                    year = years[int(batch_code[1])]
                except IndexError:
                    batch = {
                        "index": index + 1,
                        "batch_code": stripped_bc,
                        "mfg": "There was an error in batch code year"
                    }
                    converted_batch_code.append(batch)
                    continue

        except IndexError:
            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "Blank batch code"
            }
            converted_batch_code.append(batch)
            continue

            # MONTH
        try:
            if batch_code[2] not in check_month:
                batch = {
                    "index": index + 1,
                    "batch_code": stripped_bc,
                    "mfg": "There was an error in batch code month"
                }
                converted_batch_code.append(batch)
                continue

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
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "Blank batch code"
            }
            converted_batch_code.append(batch)
            continue

            # DAYS
        try:
            day_code = batch_code[3] + batch_code[4]
        except IndexError:
            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "There was an error in batch code days"
            }
            converted_batch_code.append(batch)
            continue

        if day_code not in check_days:
            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "There was an error in batch code days"
            }
            converted_batch_code.append(batch)
            continue
        else:
            day = day_code

        mfg_date = year + "-" + month + "-" + day + " 12:01:00"

        try:
            final_date = datetime.datetime.strptime(mfg_date, '%Y-%m-%d %H:%M:%S')

            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": mfg_date
            }

            converted_batch_code.append(batch)
            continue

        except:
            batch = {
                "index": index + 1,
                "batch_code": stripped_bc,
                "mfg": "Invalid date"
            }

            converted_batch_code.append(batch)
            continue
    return converted_batch_code
