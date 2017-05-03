import xml.etree.ElementTree as ET
import csv


def main():
    tree = ET.parse("vat_colormap.txt")
    root = tree.getroot()

    # open a file for writing
    vat_data = open('qgis_colormap.txt', 'w')

    # create the csv writer object
    csvwriter = csv.writer(vat_data)

    for child in range(0, len(root)):
        vat_row = []

        vat_row.append(root[child][0].text)

        # RGBA
        vat_row.append(cal_col(root[child][2].text))
        vat_row.append(cal_col(root[child][3].text))
        vat_row.append(cal_col(root[child][4].text))
        vat_row.append(255)

        label = root[child][5].text
        if label is not None:
            vat_row.append(label.replace(",", ";"))
        else:
            vat_row.append(label)

        csvwriter.writerow(vat_row)

    vat_data.close()


def cal_col(col_per):
    return int(round(float(col_per) * 255))


if __name__ == "__main__":
    main()

