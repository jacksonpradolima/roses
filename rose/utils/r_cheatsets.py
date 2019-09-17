def require_r_package(package_name):
    devtools = "devtools::install_github(\"b0rxa/scmamp\")"
    pkg = f"install.packages(\"{package_name}\", repos='https://cran-r.c3sl.ufpr.br/')"
    msg = f"\"You are missing the package '{package_name}', we will now try to install it...\""
    return """if(!require({0})){{
       print({1})
       {2}
       require({0})
    }}""".format(package_name, msg, devtools if package_name == "scmamp" else pkg)