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


class DomainTree():
    """
    This is where you define your domain tree.
    Each level is inherit from the Base
    I recommend you put root in a class Tree to handle easier.
    You should nested class to easier to define the hierarchy like in did below.
    This will make scope navigate much more easier to track.
    """
    class Root(DomainConstructor):
        def __init__(self,**kwargs):
            # this is root don't put **kwargs in because no level below
            super().__init__(None, "")
        
        class Domain_1(DomainConstructor):
            def __init__(self, domain_1_id = "+",**kwargs):
                """
                if you have any variable like local domain name dynamic, 
                put here before **kwargs, 
                the train of nested class will catch it down to root
                example here i define domain_1_id so i can change it later e.g /root/domain_1_alice/, /root/domain_1_bob/
                """
                super().__init__(
                    parent_domain = DomainTree.Root(**kwargs), # pass parent domain object train here
                    local_domain = f"{domain_1_id}" # local domain, name of this level
                )
            class Domain_1_1(DomainConstructor):
                def __init__(self, **kwargs):
                    super().__init__(
                        parent_domain = DomainTree.Root.Domain_1(**kwargs), # continue link the nested class
                        local_domain = self.__class__.__name__.lower() # local domain, name of this level
                    )
            # same level with Domain_1_1
            class Domain_1_2(DomainConstructor):
                def __init__(self, **kwargs):
                    super().__init__(
                        parent_domain = DomainTree.Root.Domain_1(**kwargs), # **kwargs will be cascade pass through whole train
                        local_domain = self.__class__.__name__.lower()
                    )

        class Domain_2(DomainConstructor):
            def __init__(self,**kwargs):
                super().__init__(
                    parent_domain = DomainTree.Root(**kwargs), 
                    local_domain = self.__class__.__name__.lower() 
                )

            class Domain_2_1(DomainConstructor):
                def __init__(self,**kwargs):
                    super().__init__(
                        parent_domain = DomainTree.Root.Domain_2(**kwargs), 
                        local_domain = self.__class__.__name__.lower() 
                    )

            class Domain_2_2(DomainConstructor):
                def __init__(self,**kwargs):
                    super().__init__(
                        parent_domain = DomainTree.Root.Domain_2(**kwargs), 
                        local_domain = self.__class__.__name__.lower() 
                    )


# now easily call them
tree = DomainTree()
root = DomainTree.Root()
domain_1_default = DomainTree.Root.Domain_1() # call domain_1 with default name
domain_1_custom = DomainTree.Root.Domain_1(domain_1_id="custom_name") # you can add the custom level name at that level
domain_1_1 = DomainTree.Root.Domain_1.Domain_1_1(domain_1_id="custom_name") # or you can add the custom level name at lower level
custom_var_at_higher_level = DomainTree.Root(domain_1_id="custom_name") # you can also pass that attribute at higher level but still no error

# now print them
string_domain = str(domain_1_default)
print("\n Print Domain:")
print("tree",tree)
print("root:",root)
print("domain_1_default:",domain_1_default)
print("domain_1_custom:",domain_1_custom)
print("domain_1_1:",domain_1_1)
print("custom_var_at_higher_level:",custom_var_at_higher_level)

print("\n Get level:")
# you can get their level
print("level of root:",root.get_level())
print("level of domain_1_default:",domain_1_default.get_level())
print("level of domain_1_custom:",domain_1_custom.get_level())
print("level of domain_1_1:",domain_1_1.get_level())
print("level of custom_var_at_higher_level:",custom_var_at_higher_level.get_level())

# you can check if domain is parent of domain
print("\n Check is parent:")
print("is root parent of domain_1_default:",root.is_parent_of(str(domain_1_default)))
print("is domain_1_default parent of domain_1_custom:",domain_1_default.is_parent_of(str(domain_1_custom)))