# PyBratabase

Bratabase API Python 3 client.

This is a synchronous client.

## Usage

Initialize a new Session pointing to the API host, `https://api.bratabase.com/`. 

It returns a new Session instance that has a `.root` document which maps
 the structure under the [API root](http://developers.bratabase.com/api-root/).

```python
from pybratabase import Session
session = Session(
    host="https://api.bratabase.com/"
)
print(session.root.links.brands.self)
https://api.bratabase.com/brands/

``` 

Each document exposes a `.meta` and `.links` member that allows to navigate
 through the API as described in the
 [schema documentation](http://developers.bratabase.com/schema/).
 

## Document types

### Entity

An [Entity](http://developers.bratabase.com/schema/#Entities) is mapped through 
an `Entity` instance that exposes its attributes under the `.body` just like 
the JSON API returns.

### Collection

[Collections](http://developers.bratabase.com/schema/#Collection) expose their
items under the `.collections` attribute. Each of these attributes contains
a _Collection tuple_, which behaves like a normal document but exposes an
additional `.entity` property that navigates to the referred entity.