# MulSet README

## Why?

## What's different

- Mappings are simpler, they are Collections of tuples
- Mappings have `keys` and `values` that are MulSet views which can also be unique, ...
- Consistency between collections
	* e.g. they all have `.add`
		- for lists this is append
		- for dicts this is adding a tuple
	* 
- Need to abstract away the store so that Mapping views can easily do everything the MulSet proper can
- Everything is ordered?
