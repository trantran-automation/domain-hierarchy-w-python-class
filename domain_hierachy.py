class DomainConstructor:
    """
    this base class to define a subdomain object
    you need to give it parent_domain so understand where it is in the hierarchy tree
    if you dont give it parent_domain it will be default as root "/"
    this will overload the local_domain
    otherwise it will inherit parent_domain and add in local_domain

    To make this class universal, output will be str with e.g: "/root/domain_1/"
    Output is str take from str(obj) or method get_domain()
    """
    def __init__(self, parent_domain:"DomainConstructor"=None, local_domain:str="", **kwargs):
        # validation, i fixed type for now
        if not isinstance(local_domain,str):
            raise TypeError(f"local_domain must be type str, got {type(local_domain).__name__}")

        # if parent is define, add a sub level, inherit from
        if isinstance(parent_domain,DomainConstructor):
            self._parent_domain:str     = parent_domain._domain
            self._level:int             = parent_domain._level + 1
            self._local_domain:str      = local_domain
            self._domain:str            = self._parent_domain + self._local_domain + "/" # domain string tree from root
        # if parent is none then this must be root domain
        else:
            self._parent_domain:str     = ""
            self._level:int             = 0
            self._local_domain:str      = "" # if parent not define then must be root
            self._domain:str            = self._parent_domain + self._local_domain + "/" # domain string tree from root

        # create inner attribute    
        self._domain_splitted:list = self.split_domain(self._domain) # this use for match domain check

        # logic attribute
        self._wild_card_match_single_lv = "+" # you can change wild card match to anything you like: #,x,...

    def __repr__(self) -> str:
        return f"BaseSubDomain(domain={self._domain}, parent_domain={self._parent_domain}, local_domain={self._local_domain}, level={self._level} )"

    def __str__(self):
        return self._domain

    def split_domain(self,input_domain:str) -> list:
        """
        E.g:
        input_domain= "/root/domain_1/domain_2/" 
        output: ["root", "domain_1, "domain_2"]
        """
        return input_domain.lstrip("/").rstrip("/").split("/")
    
    def get_domain(self) -> str:
        """
        To get full domain of this object
        """
        return self._domain
    
    def get_level(self) -> int:
        return self._level

    def is_parent_of(self,check_domain:str) -> bool:
        """
        Check Rule:
        With domain = "/root/domain_1/"
        check_domain  = "/root/domain_1/" => True # is the domain itself
        check_domain  = "/root/domain_1/domain_2/" => True # is a subdomain
        check_domain  = "/root/domain_2/" => False # different branch False
        check_domain  = "/root/" => False # higher level False

        # wild card
        With domain = "/root/+/" match any local domain this lv

        """
        check_domain_splitted = self.split_domain(check_domain)
        
        # if this is root
        if self._level == 0:
            return True

        if len(check_domain_splitted) < len(self._domain_splitted):
            # check domain is in higher level
            return False

        for level,local_domain in enumerate(self._domain_splitted):
            # check wild card match single lv
            if local_domain == self._wild_card_match_single_lv:
                continue
            # check match
            elif local_domain != check_domain_splitted[level]:
                return False
            
        return True
