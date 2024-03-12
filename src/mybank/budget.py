from pandas import DataFrame
from typing import List
from mybank.utils import filter_payments_by_text

class BudgetHeading:
    def __init__(self, name:str, include:List[str]=[], exclude:List[str]=[], 
                 case_include:bool=False, case_exclude:bool=False):
        """ Create a budget heading object
        
        Args:
        --------
        name: str
            Name of the budget heading.
        include: List[str]
            List of strings to include in the filtering.
        exclude: List[str]
            List of strings to exclude in the filtering.
        case_include: bool
            Whether to consider case when including strings.
        case_exclude: bool
            Whether to consider case when excluding strings.
        """
        self.name = name
        self.include = include
        self.exclude = exclude
        self.case_include = case_include
        self.case_exclude = case_exclude

    def filter(self, data:DataFrame) -> DataFrame:
        """ Filter the data based on the include and exclude lists
        
        Args:
        --------
        data: DataFrame
            Data to filter.
        
        Returns:
        --------
        DataFrame
            Filtered data.
        """
        return filter_payments_by_text(data, self.include, self.exclude, 
                                 self.case_include, self.case_exclude)


class Budget:
    def __init__(self, name:str, year:int, data:DataFrame, headings:List[BudgetHeading]=[]) -> None:
        self.name = name
        self.year = year
        self.data = data
        self.headings = headings

    def add_heading(self, heading:BudgetHeading) -> None:
        """ Add a heading to the budget
        
        Args:
        --------
        heading: BudgetHeading
            Budget heading to add.
        """
        self.headings.append(heading)
    
    def get_payments_without_headings(self) -> DataFrame:
        """ Get payments that do not belong to any heading
        
        Returns:
        --------
        DataFrame
            Payments that do not belong to any heading.
        """
        data = self.data.copy()
        for heading in self.headings:
            # Choose data that does not belong to the heading
            data = filter_payments_by_text(data, exclude=heading.include, 
                                           case_exclude=heading.case_include)
        return data
