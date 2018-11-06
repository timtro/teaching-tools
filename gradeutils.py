def percent_to_lettergrade(x):
  '''
  Convertert a percent grade to a letter grade. The ranges are generous—if the
  student is less than a percent from the next lettergrade, it is rounded up.
  '''
    if 0 <= x <= 49:
        return 'F'
    elif 49 < x <= 59:
        return 'D'
    elif 59 < x <= 66:
        return 'C'
    elif 66 < x <= 69:
        return 'C+'
    elif 69 < x <= 72:
        return 'B-'
    elif 72 < x <= 76:
        return 'B'
    elif 76 < x <= 79:
        return 'B+'
    elif 79 < x <= 84:
        return 'A-'
    elif 84 < x <= 89:
        return 'A'
    elif 89 < x <= 100:
        return 'A+'
    else:
        raise ValueError("Grade '" + str(x) +
                         "' cannot be translated to letter grade.")