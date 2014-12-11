import xlrd
import string


f = open('instruments/models.py', 'w')
f.write('from django.db import models\n')
f.write('from base import BaseTable\n')

instruments = open('raw_data/instruments.txt', 'r').read().split('\n')
instruments = filter(lambda i: i != '', instruments)

for instrument in instruments:

    book = xlrd.open_workbook('raw_data/%s/[%s].xlsx' % (instrument, instrument))

    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows

    col_names = list(sheet.row_values(0))

    f.write('\n\nclass %s(BaseTable):\n' % instrument)

    if nrows <= 1:
        f.write('    pass\n')

    for row in xrange(1, nrows):

        row_values = list(sheet.row_values(row))
        item = string.replace(row_values[col_names.index('item')], '.', '_')
        choices = row_values[col_names.index('choices')].split(', ')
        f.write('    %s_choices = %s\n' % (item, [(c,c) for c in choices]))
        f.write('    item_%s = models.CharField(max_length=20, choices=%s_choices, null=True)\n' % (item, item))

f.close()