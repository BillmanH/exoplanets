# Building and Rendering 3d Objects

1. build in Blender, export to GTLF format

![Alt text](../docs/img/create_mesh_sphere.png?raw=true "solar system") 

![Alt text](../docs/img/export_gtlf.png?raw=true "solar system")

2. Place in `app/static/app/objects/`


# in DEV
3. run the command line: `python manage.py collectstatic`
This will make the files available when running locally. **Note** these assets are not available on the www, and won't be available in the production app. 

4. To migrate the assets into prod
TODO: add steps to migrate to prod (when I get there). For now you can just upload them in the Azure Storage Explorer. 


