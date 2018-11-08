import unittest
import pandas as pd
from src.data_processing import clean_data, create_data_from_entry


SMALL_TEST_DATA = [
[1537549008.931, 4.5185524610000005, 4.4503286189999995, 4.4184483189999995, 4.399957745000001, 4.232904973000001, 4.364889415, 4.3492680680000015, 4.384017595, 4.3728594900000015, 4.489222585, 4.475195253000001, 4.580400243000001, 4.581037848999999, 4.647986479000001, 4.752553863000001, 4.663607826000001, 4.679547976, 4.727049623000001, 4.638103586000001, 4.598890817000001, 4.579762637000001, 4.460211512000001, 4.433750863, 4.374134702000002, 4.269886121000002, 4.376366323000001, 4.355325325000001, 4.3435296139999995, 4.367439838999999, 4.419723531000001, 4.487628570000001, 4.571473759000001, 4.619613012, 4.632365131999999, 4.7519162569999995, 4.649899297000001, 4.6983573530000005, 4.666795856, 4.665520644000001, 4.579762637000001, 4.534173808, 4.4375764989999995, 4.4713696170000015, 4.358513355, 4.286145073999999, 4.350543280000001, 4.3368347510000005, 4.347992856, 4.3728594900000015, 4.40792782, 4.515683234000001, 4.553620791000001, 4.596977999000001, 4.664564235, 4.735019698, 4.682736006000001, 4.695169323000001, 4.6833736120000005, 4.680185582000001, 4.597296802000001, 4.5507515640000005, 4.435344878, 4.429925227000001, 4.384017595, 4.299534800000001, 4.377960338, 4.3495868710000005, 4.340022781000002, 4.369352657, 4.445546574000001, 4.475195253000001, 4.5976156050000005, 4.578168622000001, 4.6425668280000005, 4.7197171540000005, 4.707921443000001, 4.671577901000001, 4.711428276, 4.6511745090000005, 4.5657353050000005, 4.5188712639999995, 4.455110663999999, 4.423230364000001, 4.422592758, 4.286782680000001, 4.348630462000002, 4.361063779, 4.358513355, 4.3645706120000005, 4.406333805000001, 4.4885849790000005, 4.583588273000001, 4.6192942089999995, 4.657231766000001, 4.733744486000001, 4.664564235, 4.699313762000001, 4.683054809000001, 4.667433462000001, 4.580400243000001],
[1537549008.986, 4.5185524610000005, 4.4503286189999995, 4.4184483189999995, 4.399957745000001, 4.232904973000001, 4.364889415, 4.3492680680000015, 4.384017595, 4.3728594900000015, 4.489222585, 4.475195253000001, 4.580400243000001, 4.581037848999999, 4.647986479000001, 4.752553863000001, 4.663607826000001, 4.679547976, 4.727049623000001, 4.638103586000001, 4.598890817000001, 4.579762637000001, 4.460211512000001, 4.433750863, 4.374134702000002, 4.269886121000002, 4.376366323000001, 4.355325325000001, 4.3435296139999995, 4.367439838999999, 4.419723531000001, 4.487628570000001, 4.571473759000001, 4.619613012, 4.632365131999999, 4.7519162569999995, 4.649899297000001, 4.6983573530000005, 4.666795856, 4.665520644000001, 4.579762637000001, 4.534173808, 4.4375764989999995, 4.4713696170000015, 4.358513355, 4.286145073999999, 4.350543280000001, 4.3368347510000005, 4.347992856, 4.3728594900000015, 4.40792782, 4.515683234000001, 4.553620791000001, 4.596977999000001, 4.664564235, 4.735019698, 4.682736006000001, 4.695169323000001, 4.6833736120000005, 4.680185582000001, 4.597296802000001, 4.5507515640000005, 4.435344878, 4.429925227000001, 4.384017595, 4.299534800000001, 4.377960338, 4.3495868710000005, 4.340022781000002, 4.369352657, 4.445546574000001, 4.475195253000001, 4.5976156050000005, 4.578168622000001, 4.6425668280000005, 4.7197171540000005, 4.707921443000001, 4.671577901000001, 4.711428276, 4.6511745090000005, 4.5657353050000005, 4.5188712639999995, 4.455110663999999, 4.423230364000001, 4.422592758, 4.286782680000001, 4.348630462000002, 4.361063779, 4.358513355, 4.3645706120000005, 4.406333805000001, 4.4885849790000005, 4.583588273000001, 4.6192942089999995, 4.657231766000001, 4.733744486000001, 4.664564235, 4.699313762000001, 4.683054809000001, 4.667433462000001, 4.580400243000001],
[1537549009.0410001, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.096, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.15, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.205, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.2589998, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.313, 4.662332613999999, 4.594427575000001, 4.530985778000001, 4.521740491000001, 4.4372576960000005, 4.37604752, 4.42067994, 4.3087800870000015, 4.335240736, 4.3492680680000015, 4.3559629310000005, 4.416535501, 4.4630807390000005, 4.5290729600000015, 4.561909668999999, 4.655956553999999, 4.6125993460000005, 4.704095807000001, 4.691981293, 4.659144584000001, 4.671577901000001, 4.607498498000001, 4.545650716000001, 4.4841217370000015, 4.440126923, 4.375728717, 4.4184483189999995, 4.301128815, 4.3668022330000005, 4.3346031300000005, 4.3817859740000005, 4.453197846000001, 4.465631163, 4.532260990000001, 4.611324134000001, 4.6403352070000015, 4.635234359000001, 4.713978700000001, 4.690068475, 4.660419796, 4.6725343100000005, 4.580081440000002, 4.555852412000001, 4.460211512000001, 4.46531236, 4.3881620340000005, 4.417173107000001, 4.3046356480000005, 4.347674053, 4.339385175, 4.3432108110000005, 4.442996150000001, 4.467862783999999, 4.541187474000001, 4.5654165020000015, 4.643523237000001, 4.606860892, 4.710153064000001, 4.671577901000001, 4.662970220000001, 4.658506978000001, 4.6167437850000015, 4.528116551000001, 4.504206326, 4.4222739550000005, 4.397726124000002, 4.4117534560000005, 4.337791160000001, 4.3368347510000005, 4.384974004000002, 4.341935599000002, 4.4586174970000005, 4.4994242810000005, 4.578168622000001, 4.537680641000001, 4.6425668280000005, 4.600484832, 4.7133410940000005, 4.693575308000001, 4.643842040000001, 4.674128325000001, 4.57689341, 4.560953260000002, 4.487309767000001, 4.4436337560000005, 4.384017595, 4.441083332000001, 4.292521133999999, 4.365527021000001, 4.355644128000002, 4.338109963000002, 4.4436337560000005, 4.479020889000001, 4.523972112000001, 4.572748971, 4.6212070270000005, 4.601122438000001, 4.675722340000001, 4.6789103700000005, 4.640972813],
[1537549009.3679998, 4.574342986, 4.545650716000001, 4.414622683000001, 4.446502983, 4.410478244000001, 4.2768997870000005, 4.3642518090000015, 4.322807419000002, 4.329821085000002, 4.408565426000001, 4.436620090000001, 4.4889037819999995, 4.586776303000001, 4.6084549070000005, 4.648305282000001, 4.7688128160000005, 4.6683898710000005, 4.690068475, 4.691024884000001, 4.591877151, 4.5612720630000005, 4.516002037000001, 4.435663681, 4.390712458, 4.421636349000001, 4.236411806, 4.3690338539999996, 4.311968117000002, 4.3562817339999995, 4.4009141540000005, 4.465949966000001, 4.496236251000001, 4.5654165020000015, 4.618975406000001, 4.630771117000001, 4.755423090000002, 4.6687086739999994, 4.691024884000001, 4.728962441000001, 4.617381391, 4.568285728999999, 4.524290915000001, 4.450966225000001, 4.405058593000001, 4.4184483189999995, 4.256177592, 4.3645706120000005, 4.340341584000002, 4.336197145000001, 4.4267371970000005, 4.432475651000001, 4.506756750000001, 4.547244731000001, 4.637465980000001, 4.605585680000001, 4.765305983000001, 4.641610419000001, 4.701864186000001, 4.685605233, 4.600484832, 4.553301988, 4.533855005, 4.426099591000001, 4.411434653000001, 4.389118443000001, 4.282000635, 4.403464578, 4.3240826310000005, 4.313880935, 4.406015002, 4.429606424000001, 4.5271601420000005, 4.572430168, 4.609092513, 4.6170625880000005, 4.751278651000001, 4.669346280000001, 4.699951368000001, 4.697400944000001, 4.590920742000001, 4.5635036840000005, 4.523972112000001, 4.442996150000001, 4.415260289000001, 4.415260289000001, 4.275305772, 4.361063779, 4.3004912090000005, 4.3432108110000005, 4.416535501, 4.426418394000001, 4.487309767000001, 4.581037848999999, 4.601760044000001, 4.649261691, 4.719398351000001, 4.696444535, 4.677953961000001, 4.7107906700000015, 4.5976156050000005],
[1537549009.4229999, 4.574342986, 4.545650716000001, 4.414622683000001, 4.446502983, 4.410478244000001, 4.2768997870000005, 4.3642518090000015, 4.322807419000002, 4.329821085000002, 4.408565426000001, 4.436620090000001, 4.4889037819999995, 4.586776303000001, 4.6084549070000005, 4.648305282000001, 4.7688128160000005, 4.6683898710000005, 4.690068475, 4.691024884000001, 4.591877151, 4.5612720630000005, 4.516002037000001, 4.435663681, 4.390712458, 4.421636349000001, 4.236411806, 4.3690338539999996, 4.311968117000002, 4.3562817339999995, 4.4009141540000005, 4.465949966000001, 4.496236251000001, 4.5654165020000015, 4.618975406000001, 4.630771117000001, 4.755423090000002, 4.6687086739999994, 4.691024884000001, 4.728962441000001, 4.617381391, 4.568285728999999, 4.524290915000001, 4.450966225000001, 4.405058593000001, 4.4184483189999995, 4.256177592, 4.3645706120000005, 4.340341584000002, 4.336197145000001, 4.4267371970000005, 4.432475651000001, 4.506756750000001, 4.547244731000001, 4.637465980000001, 4.605585680000001, 4.765305983000001, 4.641610419000001, 4.701864186000001, 4.685605233, 4.600484832, 4.553301988, 4.533855005, 4.426099591000001, 4.411434653000001, 4.389118443000001, 4.282000635, 4.403464578, 4.3240826310000005, 4.313880935, 4.406015002, 4.429606424000001, 4.5271601420000005, 4.572430168, 4.609092513, 4.6170625880000005, 4.751278651000001, 4.669346280000001, 4.699951368000001, 4.697400944000001, 4.590920742000001, 4.5635036840000005, 4.523972112000001, 4.442996150000001, 4.415260289000001, 4.415260289000001, 4.275305772, 4.361063779, 4.3004912090000005, 4.3432108110000005, 4.416535501, 4.426418394000001, 4.487309767000001, 4.581037848999999, 4.601760044000001, 4.649261691, 4.719398351000001, 4.696444535, 4.677953961000001, 4.7107906700000015, 4.5976156050000005]
]


class CleanDataTests(unittest.TestCase):

    def setUp(self):
        # Given
        self.data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )

        # When:
        self.result = clean_data(self.data)

    def test_that_GIVEN_data_THEN_the_time_is_converted_to_a_datetime_format(self):
        # Then:
        self.assertEquals(self.result["Time"].dtype, 'datetime64[ns]')


    def test_that_GIVEN_data_there_is_no_0_columns(self):
        # Then:
        self.assertTrue(0 not in self.result.columns)

    def test_that_GIVEN_data_THEN_there_are_100_columns(self):
        # Then:
        self.assertEquals(len(self.result.columns), 101)

    def test_that_GIVEN_data_set_with_duplicate_rows_THEN_the_returned_dataframe_has_no_duplicate_rows(
            self):
        # Then:
        duplicates = self.result.duplicated()
        self.assertFalse(all(duplicates))


class CreateDataFromEntryTests(unittest.TestCase):

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_first_entry_has_the_same_time_stamp(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = clean_data(data)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_timestamp = data.iloc[0]["Time"].to_datetime64()
        result_timestamp = result.iloc[0]["Time"].to_datetime64()
        self.assertEquals(result_timestamp, expected_timestamp)

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_first_entry_has_the_same_value(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = clean_data(data)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_value = 4.5185524610000005
        result_value = result.iloc[0, 0]
        self.assertEquals(expected_value, result_value)

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_second_entry_is_correct(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = clean_data(data)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_value = 4.4503286189999995
        result_value = result.iloc[1, 0]
        self.assertEquals(expected_value, result_value)
