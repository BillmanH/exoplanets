#%%
import os

functions_path = os.path.join('..','functions')

# %%
funcs = [i for i in os.listdir(functions_path) if '.' not in i]
print(f"{len(funcs)} functions found")
print(f"************************")
for i in funcs:
    print(i)

print('')
# %%


print('fetching files .. ')
for f in funcs:
    config_files = [i for i in os.listdir(os.path.join(functions_path,f)) if i=='exo_lib_config.yaml']
    if len(config_files)>0:
        print(f"fetching files for {f}")


# %%
