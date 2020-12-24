# conan-ppconsul
This repo sets up conan ppconsul

# install steps
Create packages using `conan create . mingkaic-co/stable`
For hosting, I used gitlab: see instructions https://docs.gitlab.com/ee/user/packages/conan_repository/

# usage
Before install package first add remote: `conan remote add mingkaic-co "https://gitlab.com/api/v4/projects/23299689/packages/conan"`
Add requirement `Ppconsul/<version>@mingkaic-co/stable`
