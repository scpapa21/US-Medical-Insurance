# Class to analyze the information of the patients

class Patients:
    def __init__(self, patients_df):
        self.df = patients_df
        self.ages = patients_df['age']
        self.sex = patients_df['sex']
        self.bmi = patients_df['bmi']
        self.children = patients_df['children']
        self.smoker = patients_df['smoker']
        self.region = patients_df['region']
        self.insurance_cost = patients_df['charges']
        self.patients_dictionary = {patient_id : values for patient_id, values in enumerate(zip(self.ages, self.sex, self.bmi, self.children, self.smoker, self.region, self.insurance_cost))}

        self.__create_by_sex_dict()
        self.__get_unique_regions()
        self.__calc_total_patients()
    

    # Self Calculations Methods
    def __calc_total_patients(self):
        self.total_patients = len(self.ages)
        self.total_male = len(self.by_sex_dict['male']['age'])
        self.total_female = len(self.by_sex_dict['female']['age'])

    def __create_by_sex_dict(self):
        by_sex_dict =  {'male': {'age' : [], 'bmi' : [], 'children' : [], 'smoker' : [], 'region' : [], 'insurance_cost' : []}, 
                           'female': {'age' : [], 'bmi' : [], 'children' : [], 'smoker' : [], 'region' : [], 'insurance_cost' : []}}

        for patient_id in self.patients_dictionary:
            patient_info = self.patients_dictionary[patient_id]
            by_sex_dict[patient_info[1]]['age'].append(patient_info[0]) 
            by_sex_dict[patient_info[1]]['bmi'].append(patient_info[2]) 
            by_sex_dict[patient_info[1]]['children'].append(patient_info[3]) 
            by_sex_dict[patient_info[1]]['smoker'].append(patient_info[4]) 
            by_sex_dict[patient_info[1]]['region'].append(patient_info[5])
            by_sex_dict[patient_info[1]]['insurance_cost'].append(patient_info[6]) 
        
        self.by_sex_dict = by_sex_dict
    
    def __get_unique_regions(self):
        self.unique_regions = list(self.region.unique())


    # Data description
    def data_description(self):
        print('\nData Description:')
        return self.df.describe()
    
    def data_correlation(self):
        print('\nData Correlation:')
        df_updated = self.df.copy(True)

        df_updated.loc[df_updated['sex'] == 'male', 'sex'] = 1
        df_updated.loc[df_updated['sex'] == 'female', 'sex'] = 0

        df_updated.loc[df_updated['smoker'] == 'yes', 'smoker'] = 1
        df_updated.loc[df_updated['smoker'] == 'no', 'smoker'] = 0

        df_updated.drop('region', axis=1, inplace=True)
        
        return df_updated.corr()
    

    # Base Analysis
    def base_analysis(self):
        result = '\nBase Analysis:\n'

        average_bmi = round(self.__calc_average_bmi(),2)
        average_children = round(self.__calc_average_children(),2)
        average_cost = round(self.__calc_average_cost(),2)

        result += f'There are {self.total_patients} total patients, {self.total_male} male and {self.total_female} female.\n'
        result += f'In average they have {average_children} children, {average_bmi} bmi and ${average_cost} insurance cost;'
        
        return result
    
    def __calc_average_bmi(self):
        return sum(self.bmi) / len(self.bmi)

    def __calc_average_children(self):
        return sum(self.children) / len(self.children)
    
    def __calc_average_cost(self):
        return sum(self.insurance_cost) / len(self.insurance_cost)


    # Age Analysis
    def age_analysis(self):
        result = '\nAge Analysis:\n'

        age_average = round(self.__calc_age_average(),2)
        male_age_average = round(self.__calc_age_average_by_sex('male'),2)
        female_age_average = round(self.__calc_age_average_by_sex('female'),2)
        age_cost_correlation = round(self.__calc_age_cost_correlation(),3)

        result += f'The average age of the patients is {age_average}.\n'
        result += f'For males is {male_age_average} and for females is {female_age_average}.\n'
        result += f'The correlation between age and the insurance cost is {age_cost_correlation}.'

        return result
    
    def __calc_age_average(self):
        return sum(self.ages)/self.total_patients

    def __calc_age_average_by_sex(self, sex):
        patients_by_sex = self.__calc_total_by_sex(sex)
        return sum(self.by_sex_dict[sex]['age'])/patients_by_sex
    
    def __calc_age_cost_correlation(self):
        return self.ages.corr(self.insurance_cost)
    
    
    # Sex Analysis
    def sex_analysis(self):
        result = '\nSex Analysis:\n'

        male_children_average = round(self.__calc_average_children_by_sex('male'),2)
        female_children_average = round(self.__calc_average_children_by_sex('female'),2)

        male_bmi_average = round(self.__calc_average_bmi_by_sex('male'),2)
        female_bmi_average = round(self.__calc_average_bmi_by_sex('female'),2)

        male_insurance_cost_average = round(self.__calc_average_insurance_cost_by_sex('male'),2)
        female_insurance_cost_average = round(self.__calc_average_insurance_cost_by_sex('female'),2)

        male_insurance_cost_correlation = round(self.__calc_sex_cost_correlation('male'),3)
        female_insurance_cost_correlation = round(self.__calc_sex_cost_correlation('female'),3)

        result += f'Average number of children for males is {male_children_average}, for females is {female_children_average}.\n'
        result += f'The average bmi for males is {male_bmi_average}, for females is {female_bmi_average}.\n'
        result += f'Average insurance cost for males is ${male_insurance_cost_average}, for females is ${female_insurance_cost_average}.\n'
        result += f'The correlation between being a male and the insurance cost is {male_insurance_cost_correlation}.\n'
        result += f'While the correlation between being a female and the insurance cost is {female_insurance_cost_correlation}.'

        return result

    def __calc_total_by_sex(self, sex : str):
        return self.sex.value_counts()[sex]
    
    def __calc_average_children_by_sex(self, sex : str):
        patients_by_sex = self.__calc_total_by_sex(sex)
        return sum(self.by_sex_dict[sex]['children'])/patients_by_sex
    
    def __calc_average_bmi_by_sex(self, sex : str):
        patients_by_sex = self.__calc_total_by_sex(sex)
        return sum(self.by_sex_dict[sex]['bmi'])/patients_by_sex

    def __calc_average_insurance_cost_by_sex(self, sex : str):
        patients_by_sex = self.__calc_total_by_sex(sex)
        return sum(self.by_sex_dict[sex]['insurance_cost'])/patients_by_sex
    
    def __calc_sex_cost_correlation(self, sex_used : str):
        sex_df_updated = self.df.copy(True)
        sex_df_updated.drop(['age','bmi','children','smoker','region','charges'], axis=1, inplace=True)

        if sex_used == 'male':
            sex_df_updated.loc[sex_df_updated['sex'] == 'male', 'sex'] = 1
            sex_df_updated.loc[sex_df_updated['sex'] == 'female', 'sex'] = 0
        else:
            sex_df_updated.loc[sex_df_updated['sex'] == 'male', 'sex'] = 0
            sex_df_updated.loc[sex_df_updated['sex'] == 'female', 'sex'] = 1

        sex_updated = sex_df_updated['sex']

        return sex_updated.corr(self.insurance_cost)


    # Smoker Analysis
    def smoker_analysis(self):
        result = '\nSmoker Analysis:\n'

        male_smokers = self.__calc_smokers_by_sex('male')
        female_smokers = self.__calc_smokers_by_sex('female')

        male_smokers_percentage = round(self.__calc_smoker_percentage_by_sex(male_smokers, 'male'),4)*100
        female_smokers_percentage = round(self.__calc_smoker_percentage_by_sex(female_smokers, 'female'),4)*100

        smoker_cost_correlation = round(self.__calc_smoker_cost_correlation(),3)
        smoker_average_cost = round(self.__calc_average_insurance_cost_if_smoker(True),2)
        non_smoker_average_cost = round(self.__calc_average_insurance_cost_if_smoker(False),2)

        result += f'There are {male_smokers} male smokers, this represents {male_smokers_percentage}% of males.\n'
        result += f'For females there are {female_smokers} smokers, that represent {female_smokers_percentage}% of females.\n'
        result += f'The correlation between smoking and the insurance cost is {smoker_cost_correlation}.\n'
        result += f'This is evident in the average insurance cost of a smoker: ${smoker_average_cost} compared to the insurance cost of a non smoker: ${non_smoker_average_cost}.'
        
        return result

    def __calc_smokers_by_sex(self, sex : str):
        smoker_count = self.by_sex_dict[sex]['smoker'].count('yes')
        return smoker_count
    
    def __calc_smoker_percentage_by_sex(self, smokers : int, sex : str):
        patients_by_sex = self.__calc_total_by_sex(sex)
        return smokers / patients_by_sex

    def __calc_smoker_cost_correlation(self):
        smoker_df_updated = self.df.copy(True)
        smoker_df_updated.drop(['age','bmi','children','region','charges'], axis=1, inplace=True)

        smoker_df_updated.loc[smoker_df_updated['smoker'] == 'yes', 'smoker'] = 1
        smoker_df_updated.loc[smoker_df_updated['smoker'] == 'no', 'smoker'] = 0

        smoker_updated = smoker_df_updated['smoker']

        return smoker_updated.corr(self.insurance_cost)

    def __calc_average_insurance_cost_if_smoker(self, is_smoker : bool):
        smokes_cost_dict = {'yes' : [], 'no' : []}

        for smoker, cost in zip(self.smoker, self.insurance_cost):
            if smoker == 'yes':
                smokes_cost_dict['yes'].append(cost)
            else:
                smokes_cost_dict['no'].append(cost)

        if is_smoker:
            smokes = 'yes'
        else:
            smokes = 'no'

        smoker_total = self.by_sex_dict['male']['smoker'].count(smokes) + self.by_sex_dict['female']['smoker'].count(smokes)
    
        return sum(smokes_cost_dict[smokes])/smoker_total


    # Region Analysis
    def regions_analysis(self):
        result = '\nRegions Analysis:\n'

        for region in self.unique_regions:
            smokers_in_region = self.__calc_smokers_by_region(region)
            cost_in_region = round(self.__calc_cost_by_region(region),2)
            result += f'In the {region} there are {smokers_in_region} smokers. The average cost of insurance in this region is of ${cost_in_region}.\n'

        return result
    
    def __calc_smokers_by_region(self, region_used : str):
        smokers_by_region_dict = {region : [] for region in self.unique_regions}
        regions_smoker_info = zip(self.region, self.smoker)

        for region, smoker in regions_smoker_info:
            if smoker == 'yes':
                smokers_by_region_dict[region].append(1)

        return sum(smokers_by_region_dict[region_used])

    def __calc_cost_by_region(self, region_used : str):
        cost_by_region_dict = {region : [] for region in self.unique_regions}
        regions_cost_info = zip(self.region, self.insurance_cost)

        for region, cost in regions_cost_info:
            cost_by_region_dict[region].append(cost)

        return sum(cost_by_region_dict[region_used]) / len(cost_by_region_dict[region_used])


    # Complete Analysis
    def analysis_results(self):
        print(self.base_analysis())
        print(self.age_analysis())
        print(self.sex_analysis())
        print(self.smoker_analysis())
        print(self.regions_analysis())

        print(self.data_description())
        print(self.data_correlation())
    
    

