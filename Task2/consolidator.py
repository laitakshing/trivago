import os
import json
import sys


class Consolidate_recommendation:
    def __init__(self, partner_loc, priority_loc):
        '''
        Get the location path of partner list and priority list
        '''
        self.partner_loc = partner_loc
        self.priority_loc = priority_loc

    def read_input_files(self):
        '''
        Read the path and return partner details list and priority list 
        '''
        try:
            # type:(str,str) -> list,list
            with open(self.partner_loc, 'r') as p:
                self.partner_l = eval(p.read().strip())
            with open(self.priority_loc, 'r') as p:
                self.priority_l = eval(p.read().strip())
            return self.partner_l, self.priority_l
        except Exception as e:
            print(e)
            return None

    def consolidate(self):
        # type:(list,list) -> dict
        """
        Details consolidation logic:
        1. Create a temp index list 
        2. for every item in parnter list, get the index(i.e. ranking from 0 to len(priority list)-1)
        3. Assume that exist some partner is not in priority list, we use try/excpet to handle this case and assign the ranking = 100 (max rank = 99 so 100 is the exceptional case)
        4. Get the mininum index(i.e. highest rank) and assign the index to min_index
        5. condition "min_index < 100" is to ensure at least one parnter is in priority list
        6. Get only accommodation_name in accommodation_data and remove partner_name
        7. If we cannot find any partner within priority list, return None

        Assumption:
        1. If duplicated partner are found in partner list, we assume the hotel name would be same.
        2. The input format should be same as the example stated in assignment.

        Args:
            partner_list (list): partner detail list
            priority_list (list): priority ranking list
        """
        self.temp_index_list = []
        for item in self.partner_l:
            try:
                self.temp_index_list.append(
                    self.priority_l.index(item['partner_name']))
            except:
                self.temp_index_list.append(100)
        min_index = self.temp_index_list.index(min(self.temp_index_list))
        if min(self.temp_index_list) < 100:  # i.e. we can find a partner within priority list
            result = {
                k: v for k, v in self.partner_l[min_index].items() if k != 'partner_name'}
            result['accommodation_data'] = {
                k: v for k, v in result['accommodation_data'].items() if k == 'accommodation_name'}
            return result
        else:
            print('No partner can be found within priority list.')
            return None


if __name__ == "__main__":
    partner_loc = input(
        "Please enter the location of partner file, the file should contain the list of collection of dictionary: (e.g./Users/tak/Desktop/partner.txt)\n")
    priority_loc = input(
        "Please enter the location of priority_file, the file should contain the list of partner in priority order: (e.g./Users/tak/Desktop/priortiy.txt)\n")
    C = Consolidate_recommendation(partner_loc, priority_loc)
    if not C.read_input_files():
        sys.exit(0)
    print('Result: \n {}'.format(C.consolidate()))
