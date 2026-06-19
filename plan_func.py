from random import randint

def totalTime(exerciseOptions):
    time = 0
    for index in range(len(exerciseOptions)):
        time += exerciseOptions[index]['time']
    return time*2

def makePlan(formResponse, exerciseOptions):
    '''Expected parameters:
    1 - {} - Answers of qs
    2 - {} - All exercises in db, w details, filtered by checking equipment availability
    '''
    print('form response is', formResponse)
    print('exercises are', exerciseOptions)

    #Format time
    if formResponse['time'].endswith('minutes'):
        formResponse['time'] = int(formResponse['time'][0:3])*60
    else:
        formResponse['time'] = int(formResponse['time'][0:2])*60*60

    # # Combine exerciseOptions & equipment
    # exerciseOptions = []
    # for ex in exercises:
    #     if ex['needs_eq']:
    #         for eq in equipment:
    #             if ex['name'] in eq['name']:
    #                 exerciseOptions.append(ex)
    #                 break
    #     else:
    #         exerciseOptions.append(ex)
    deleteHard = False
    if formResponse['difficulty'] == 'easy':
        deleteHard = True
    
    new_options = []
        
    # Filter options
    for index in range(len(exerciseOptions)):
        ex = exerciseOptions[index]
        exerciseOptions[index]['time'] = int(exerciseOptions[index]['time'])
        if deleteHard:
            if ex['difficulty'] == 'hard':
                continue
        for target in formResponse['target_areas']:
            if target in ex['target_areas']:
                new_options.append(exerciseOptions[index])
                break

    final_options = new_options.copy()

    # To handle tiny workout times with large dataset
    rep_bool = 0
    while totalTime(final_options) > formResponse['time']:
        index = randint(0, len(final_options)-1)
        if type(final_options[index]['reps']) == bool:
                if rep_bool:
                    final_options.pop(index)
                    rep_bool = not rep_bool
        else:
            final_options[index]['time'] = ex['time']/2

    # To increase reps/time until target time
    while totalTime(final_options) < formResponse['time']:
        for index in range(len(final_options)):
            ex = final_options[index]
            if ex['reps']:
                final_options[index]['time'] += ex['time']*5
                if type(final_options[index]['reps']) == bool:
                    final_options[index]['reps'] = 5
                else:
                    final_options[index]['reps'] += 5
            else:
                final_options[index]['time'] += ex['time']*1.5

    return final_options
                
    