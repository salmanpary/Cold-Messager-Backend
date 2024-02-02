# name, location,latest_company_name, latest_company_role, latest_company_years_of_experience, first_top_skill, second_top_skill, latest_volunteering_experience

class ColdMessage():
    def __init__(self,template,extracted_data):
        self.template = template
        self.extracted_data = extracted_data
        self.message = template
        self.variables = {}
        self.get_vars()

    def get_vars(self):
        data_keys = self.extracted_data.keys()
        if 'name' in data_keys and len(self.extracted_data['name']) != 0:
            self.variables['name'] = self.extracted_data['name']

        if 'location' in data_keys and len(self.extracted_data['location']) != 0:
            self.variables['location'] = self.extracted_data['location']

        if 'experience' in data_keys and len(self.extracted_data['experience']) != 0:
            latest_company = self.extracted_data['experience'][0]
            latest_company_keys = latest_company.keys()
            self.variables['latest_company_name'] = latest_company['company_name']
            if 'roles' in latest_company_keys and latest_company['roles'] != 0:
                self.variables['latest_company_role'] = latest_company['roles'][0]['role']
            if 'primary_info' in latest_company_keys:
                if 'duration' in latest_company['primary_info'].keys():
                    self.variables['latest_company_years_of_experience'] = latest_company['primary_info']['duration']
        
        if 'top_skills' in data_keys and len(self.extracted_data['top_skills']) != 0:
            skills_fields = ['first_top_skill','second_top_skill']
            for i in range(2):
                self.variables[skills_fields[i]] = self.extracted_data['top_skills'][i]

        if 'volunteering_experience' in data_keys and len(self.extracted_data['volunteering_experience']) != 0:
            self.variables['latest_volunteering_experience'] = self.extracted_data['volunteering_experience'][0]['role']

    def generate_message(self):
        for variable in self.variables.keys():
            variable_ = '{{' + variable + '}}'
            if variable_ in self.message:
                self.message = self.message.replace(variable_,self.variables[variable])
        return self.message