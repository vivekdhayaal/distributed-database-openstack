cd ~/stack/tempest
for i in test_default_project_id test_domains test_list_projects test_list_users test_users test_groups test_roles test_projects test_projects_negative
do
    echo ==============
    echo "$i"
    echo ==============
    python -m testtools.run tempest.api.identity.admin.v3.$i
done
