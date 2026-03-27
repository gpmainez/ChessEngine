import os
import sys

def filter_env_vars(env_dict, filters):

       
    if not filters:
        return dict(sorted(env_dict.items()))
        
    filtered_result = {}
    filters_lower = []
    for f in filters:
        filters_lower.append(f.lower())
    for key, value in env_dict.items():
        key_lower = key.lower()
        for f in filters_lower:
            if f in key_lower:
                filtered_result[key] = value
                break
    sorted_vars = dict(sorted(filtered_result.items())) #konwertujemy z powrotem na slownik (z listy krotek) bo slownik ma O(1) dla wyszikiwania
    return sorted_vars

def main():
    args = sys.argv[1:]
    result = filter_env_vars(os.environ, args)
    
    for key, value in result.items():
        print(f"{key}={value}\n")

if __name__ == "__main__":
    main()