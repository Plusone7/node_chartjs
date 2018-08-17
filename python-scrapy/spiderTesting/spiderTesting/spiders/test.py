import json

d = [
{
"featureName":"designed for",
"featureDescription":"Run"
},
{
"featureName":"essentials pocket ",
"featureDescription":"Store your must-haves in an interior pocket"
},
{
"featureName":"CONTINUOUS DRAWCORD",
"featureDescription":"Won't get pulled inside or lost in the wash"
},
{
"featureName":"medium-rise",
"featureDescription":"Higher rise increases coverage and comfort"
},
{
"featureName":"INSEAM",
"featureDescription":"4\""
},
{
"featureName":"lycra\u00ae",
"featureDescription":"Added Lycra\u00ae fibre for stretch and shape retention"
},
{
"featureName":"lightweight liner",
"featureDescription":"Built-in lightweight liner is designed to stay in place"
},
{
"featureName":"Comfortable waistband",
"featureDescription":"Lies flat against your skin and won't dig in"
}
]

for i in d[-2:]:
    print(i['featureName'])

