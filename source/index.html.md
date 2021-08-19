---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  # - shell
  # - ruby
  - python
  # - javascript

toc_footers:
  - <a href='http://flapjack.rudge-lab.org/'>Sign Up to Flapjack</a>
  - <a href='https://github.com/slatedocs/slate'>Documentation Powered by Slate</a>

includes:
#  - errors

search: true

code_clipboard: true
---

# Flapjack Python Package

This document covers the basics of how to use the Flapjack Python Package. Keep in mind that you are only able to access studies to which: you are the owner of, studies that has been previously shared with you, or public studies.

This example API documentation page was created with [Slate](https://github.com/slatedocs/slate).

# Importing Flapjack

```python
import flapjack
from flapjack import Flapjack
```

To import Flapjack you need to use the command on the side.

# Connecting to Flapjack

```python
fj=Flapjack(‘flapjack.rudge-lab.org:8000’)
```
> After the Flapjack object has been created you have to log-in, using the following command:

```python
fj.log_in(username=user, password=passwd)
```
> If the username or password are not found or erroneous, you will get the following error: <br>
> `TypeError: 'int' object is not subscriptable`

The Flapjack package works by creating an object called flapjack, which is the connection to the system, and where you can specify which instance –either online or offline– you want to connect to, in this example we are connecting to Flapjack’s main instance.

# Flapjack's models

The possible models that you can specify, and its attributes are as follows.

<a name="Table1"></a>
Table 1. Flapjack’s models and their attributes. Attributes in _italics_ are optional when creating its model.

| Model | Attributes |
| -: | :- |
| study | name <br> description <br> _doi_ <br> _owner_ <br> _shared_with_ <br> public |
| assay | study <br> name <br> machine <br> description <br> temperature |
| media | owner <br> name <br> description |
| strain | owner <br> name <br> description |
| chemical | owner <br> name <br> description <br> _pubchemid_ |
| supplement | owner <br> name <br> chemical <br> concentration |
| dna | owner <br> name <br> _sboluri_ |
| vector | owner <br> name <br> dnas |
| sample | assay <br> _media_ <br> _strain_ <br> _vector_ <br> supplements <br> row <br> col |
| signal | owner <br> name <br> description <br> color |
| measurement | sample <br> signal <br> value <br> time |

# Functions

The Flapjack package provides several functions to access the database, and you are able to manipulate them as long as you have permission. Bear in mind that these functions are HTTPS requests.

## 1. Create Function

```python
study = fj.create('study', name='Test study', description='This is a test')
```

This function allows you to create a new object. Take into consideration that it is necessary to specify all the information needed to create the object, otherwise you will get an error. Refer to [Table 1](#Table1).

`variable_name = fj.create('model', attribute_1=value_1, attribute_n=value_n)`

Where `variable_name` is the assigned name for easy later access. `fj.create` states that the create function is being called. The values accepted for `model` and `attribute` are listed in [Table 1](#Table1), and `value` is the value you wanted to assign to the corresponding attribute.

<aside class="warning">
Consider that you have to provide every attribute required to the model you are interested in creating, otherwise you’ll get an error.
</aside>

On the side there is an example of using the create function to create a study called “Test study” and with description “This is a test”:

Take into account that in this example we only provided values for name and description, because these values are required as shown in [Table 1](#Table1).

## 2. Get Function

```python
study = fj.get('study', name='Context effects')
```
><aside class="notice">
>If you specify a value that is not present in the studies that you have access, like writing a wrong name for example, an <code>Empty DataFrame</code> will be retrieved.
></aside>

><aside class="notice">
>If you type a model that is not present in Flapjack, like typing "studt" instead of "study" you will get an error stating <code>model studt does not exist</code>
></aside>

This function retrieves data from a particular table in the database.

`variable_name = fj.get('model', attribute=value)`

Where `variable_name` is the assigned name for easy later access. `fj.get` states that the get function is being called. The values accepted for `model` and `attribute` are listed in [Table 1](#Table1), and `value` is the value you are looking for.
On the right there is an example of using the get function to find a study called Context effects.

The output of this function is a Pandas DataFrame.

## 3. Patch Function

```python
study = fj.patch('study', study.id[0], name='Changed name')
```

><aside class="notice">
>If you type a model that is not present in Flapjack, like typing "studt" instead of "study" you will get an error stating <code>Problem modifying studt</code>
></aside>

><aside class="notice">
>If you type a nonexistant id you will get an error stating <code>KeyError</code>
></aside>

This function allows you to modify something that already exists. You have to specify the model id.

`variable_name = fj.patch('model', model.id[id_number], attribute=value)`

Where `variable_name` is the assigned name for easy later access. `fj.patch` states that the patch function is being called and `id_number` is the id of the study at which the attributes are to be modified. The values accepted for `model` and `attribute` are listed in [Table 1](#Table1), and `value` is the new value you want to assign.

On the size there is an example where we modify the name of the study with id = 0 to “Changed name”.

## 4. Delete Function

```python
deleting_study = fj.delete('study', study.id[0])
```
> The following message asking for confirmation will be displayed: <br>
> `If you are sure you want to delete study with id=0 type "yes"`

><aside class="notice">
>If you type a nonexistant id you will get an error stating <code>KeyError</code>
></aside>

Allows you to delete the object. You have to specify the model id.

```variable_name = fj.delete('model', model.id[id_number])```

Where `variable_name` is the assigned name for easy later access. `fj.delete` states that the delete function is being called and `id_number` is the id of the model at which the attributes are to be modified. The values accepted for `model` and `attribute` are listed in [Table 1](#Table1).

On the right sized there is an example of deleting an study with id = 0.

This function retrives a boolean value.

## 5. Analysis Function

```python
analyzing = fj.analysis(study=study.id,vector=vector_id,
media=media_id,
strain=strain_id,
type='Expression Rate (inverse)',
eps=1e-2, n_gaussians=12, biomass_signal=od.id, )
```
> With this function you can query any of the models described in [Table 1](#Table1). In this example, study, vector, media, and strain compose the query parameters, which gives us a certain combination of data from the database.

This function analyze data from a particular table in the database.

`variable_name = fj.analysis('model', type=value, 'parameters')`

Where `variable_name` is the assigned name for easy later access. `fj.analysis` states that the analysis function is being called. The values accepted for `model` are listed in [Table 1](#Table1), and `value` and `parameters` are the type of analysis you want to perform and its requiered parameters, respectively. You can see the full list of available analysis and its parameters in the table bellow.

<a name="Table2"></a>
Table 2. Type of analysis available in Flapjack.

| Analysis | Parameters |
| -: | :- |
| Velocity | `df` = data frame to analyse <br> `pre_smoothing` = Savitsky-Golay filter parameter (window size) <br> `post_smoothing` = Savitsky-Golay filter parameter (window size) |
| Expression Rate (indirect)  | df <br> density_df <br> pre_smoothing <br> post_smoothing |
| Expression Rate (direct) |  |
| Expression Rate (inverse) | eps <br> n_gaussians <br> biomass_signal |
| Mean Velocity |  |
| Max Velocity |  |
| Mean Expression |  |
| Max Expression |  |
| Induction Curve |  |
| Heatmap |  |
| Kymograph |  |
| Alpha |  |
| Rho |  |
| Background Correct |  |

The output of this function is a Pandas DataFrame, similar to the one shown bellow.

|  | Signal_id | Signal | Color | Measurement | Time | Sample | Assay | Study | Media | Strain | Supplement1 | Chemical1 | Chemical_id1 | Concentration |
| -: | -: | -: | - | -: | - | -: | - | - | -: | - | -: | -: | -: | -: |
| 0 | 2 | OD | black | 0.00050 | 0.194444 | 1374 | c1 rep1 | Context | M9-glucose | MG1655z1 | NaN | NaN | NaN | NaN|

On the right there is an example of an Expression Rate (inverse) analysis.

## 6. Plot Function

```python
figure = fj.plot(study=study.id,vector=vector_id, media=media_id, strain=strain_id,
type='Expression Rate (inverse)', eps=1e-2, n_gaussians=12, biomass_signal=od.id, normalize='Mean/std', subplots='Media', markers='Signal', plot='Mean/std')
```
> In this example, <code>normalize='Mean/std'</code>, <code>subplots='Media'</code>, <code>markers='Signal'</code>, and <code>plot='Mean/std</code> are used as the plotting options.

><aside class="notice">
>You can type <code>None</code> as <code>type</code> to view all the raw data.
></aside>

This function allows you to plot data.

This function analyze data from a particular table in the database.

`variable_name = fj.analysis('model', type=value, 'parameters', plotting_options)`

Where `variable_name` is the assigned name for easy later access. `fj.analysis` states that the analysis function is being called. The values accepted for `model` are listed in [Table 1](#Table1), `value` and `parameters` are the type of analysis you want to perform and its requiered parameters, respectively. You can see the full list of available analysis and its parameters in [Table 2](#Table2). Finally, `plotting_options` -as their name states- are the options for the plot you want to obtain, the full list of plotting option keys is available bellow.

<a name="Table3"></a>
Table 3. List of plotting options keys and its parameters.

| Plot option keys | Parameters |
| -: | :- |
| plot_type | timeseries <br> bar <br> induction <br> heatmap <br> kymograph |
| normalize | Mean/std |
| subplots | Media |
| markers | Signal |
| plot | Mean/std |

The output of this function is a Plotly plot.