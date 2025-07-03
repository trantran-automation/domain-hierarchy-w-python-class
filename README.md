# domain-hierarchy-w-python-class
A short script to demonstrate a convince way to define domain name hierarchy with python class.
This project is for people who work with a lot of domain syntax like /root/amr/action/.. like in ROS and MQTT.
If you tired of have to remember every domain, sub domain, here is a way to help you define it easy, robust, friendly with Pylance, code hint

## Feature:
- Create a domain class to handle domain name hierarchy instead of pure string
- Help you define a hierarchy tree of domain name with python nested class.
- Allow custom, dynamic local domain name when define the tree
- Has a "is_parent_of" method to match sub domain, peer domain with a domain in str form

# Usage
- First declare your tree in any file
```python
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

  
```
You can then import it everywhere like any python class
- I let the local domain is lowercase of that `self.__class__.__name__.lower() ` for convince
- You can create a dynamic, many variable local name like below
```python
class Domain_1(DomainConstructor):
            def __init__(self, domain_1_id = "+",**kwargs):
                super().__init__(
                    parent_domain = DomainTree.Root(**kwargs), # pass parent domain object train here
                    local_domain = f"{domain_1_id}" # local domain, name of this level
                )
```
- To call your domain:
```python
tree = DomainTree()
root = DomainTree.Root()
domain_1_default = DomainTree.Root.Domain_1() # call domain_1 with default name
domain_1_custom = DomainTree.Root.Domain_1(domain_1_id="custom_name") # you can add the custom level name at that level
domain_1_1 = DomainTree.Root.Domain_1.Domain_1_1(domain_1_id="custom_name") # or you can add the custom level name at lower level
custom_var_at_higher_level = DomainTree.Root(domain_1_id="custom_name") # you can also pass that attribute at higher level but still no error
```

- Convert to string simplicity with str(), also you can print them because method `__str__` have been overload to return full domain string.
```python
string_domain = str(domain_1_default)
print("\n Print Domain:")
print("tree",tree)
print("root:",root)
print("domain_1_default:",domain_1_default)
print("domain_1_custom:",domain_1_custom)
print("domain_1_1:",domain_1_1)
print("custom_var_at_higher_level:",custom_var_at_higher_level)
```
- You can get the level of domain object with method get_level()

```python
print("level of root:",root.get_level())
print("level of domain_1_default:",domain_1_default.get_level())
print("level of domain_1_custom:",domain_1_custom.get_level())
print("level of domain_1_1:",domain_1_1.get_level())
print("level of custom_var_at_higher_level:",custom_var_at_higher_level.get_level())
```

- Check whether the domain string is a child of a domain object

```python
print("\n Check is parent:")
print("is root parent of domain_1_default:",root.is_parent_of(str(domain_1_default)))
print("is domain_1_default parent of domain_1_custom:",domain_1_default.is_parent_of(str(domain_1_custom)))
```