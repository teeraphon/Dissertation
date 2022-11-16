import matplotlib.pyplot as plt
import numpy as np

respond_time_N10 = [
    3.9238789081573486,
    5.252431154251099,
    6.479323148727417,
    7.212996959686279,
    8.49918508529663,
    10.126832246780396,
    11.62595796585083,
    13.461657047271729,
    14.580891847610474,
    15.575928926467896,
    16.04611611366272,
    17.039019107818604,
    17.47286605834961,
    17.871481895446777,
    18.29424285888672,
    18.60822296142578,
    19.834725856781006,
    19.985033988952637,
    20.491005182266235,
    21.007036924362183,
    21.478130102157593,
    21.83872699737549,
    22.907679796218872,
    22.945525884628296,
    23.241262912750244,
    23.61998677253723,
    24.41111707687378,
    24.76398801803589,
    26.95768690109253,
    26.60339093208313,
    27.012324810028076,
    26.837329864501953,
    28.023152828216553,
    29.23727583885193,
    28.967411041259766,
    29.635541915893555,
    30.133424043655396,
    30.975213050842285,
    31.214195251464844,
    31.688544034957886,
    32.27992296218872,
    32.94830298423767,
    33.70117115974426,
    34.370012283325195,
    34.57665491104126,
    34.85123372077942,
    35.87910485267639,
    36.98908710479736,
    36.675729274749756,
    36.60175800323486,
    37.57588720321655,
    37.92903923988342,
    38.08418583869934,
    39.23455214500427,
    39.564943075180054,
    40.67650508880615,
    40.61243486404419,
    42.21889877319336,
    41.58737802505493,
    42.45991516113281,
    42.354265213012695,
    43.689669132232666,
    43.35965609550476,
    44.71376609802246,
    45.02116298675537,
    46.18618702888489,
    46.33038091659546,
    46.75313377380371,
    48.9701509475708,
    48.377275705337524,
    49.16215991973877,
    49.35957717895508,
    49.61571979522705,
    50.59894299507141,
    52.709352016448975,
    52.23422908782959,
    52.11439514160156,
    52.99301505088806,
    52.93217992782593,
    53.51202893257141,
    53.52727699279785,
    54.568166971206665,
    54.98763108253479,
    55.33240985870361,
    56.64707398414612,
    67.0996961593628,
    64.08538818359375,
    63.83901906013489,
    61.89102792739868,
    60.633177757263184,]
respond_times_N50 = [4.771154403686523, 8.306429862976074, 12.106808185577393, 11.77746319770813, 14.847284078598022, 16.506481885910034, 20.15147590637207, 20.43464493751526, 23.040216207504272, 23.815505981445312, 26.426106214523315, 26.881540298461914, 29.914103031158447, 31.470746994018555, 36.060264110565186, 38.26970911026001, 37.71008491516113, 42.48465895652771, 40.29033899307251, 48.97690272331238, 46.583839893341064, 54.66207194328308, 55.206255197525024, 58.119524002075195, 63.948296785354614, 62.8645920753479, 63.70095705986023, 63.49399995803833, 68.92336416244507, 68.04919576644897, 68.49473714828491, 69.84501576423645, 70.42189812660217, 77.89622402191162, 74.7980649471283, 76.20775294303894, 77.50238180160522, 83.28265476226807, 79.89081597328186, 79.04616022109985, 81.37743210792542, 82.55306792259216, 87.77866387367249, 88.38699221611023, 90.47835397720337, 89.63706111907959, 94.27828598022461, 95.60876297950745, 102.3271369934082, 106.21137118339539, 105.64992213249207, 108.69004702568054, 112.43849396705627, 117.64636993408203, 115.37761616706848, 118.07922410964966, 117.22361493110657, 115.45214223861694, 126.41206979751587, 124.77209305763245, 126.2344868183136, 135.11713004112244, 129.3978910446167, 128.85613989830017, 132.82179498672485, 133.6894588470459, 137.65779495239258, 143.82085394859314, 139.03080582618713, 141.86368799209595, 143.86211681365967, 156.0609209537506, 157.49433398246765, 149.41979479789734]
print(len(respond_times_N50))
respond_time_N100 = [6.649109840393066, 10.259104013442993, 14.379979133605957, 21.302656888961792, 24.27684187889099, 26.68130111694336, 28.017656087875366, 35.749855041503906, 35.71391296386719, 37.17029619216919, 38.13596200942993, 42.29883170127869, 41.14655113220215, 39.170433044433594, 42.8798668384552, 46.41788983345032, 49.54980731010437, 52.725037813186646, 68.61562299728394, 64.48024702072144, 75.58595180511475, 70.09487891197205, 95.2917799949646, 114.51266813278198, 116.29983592033386, 125.89039492607117, 128.25083088874817, 145.11356711387634, 135.77104878425598, 125.28478217124939, 112.77962708473206, 115.57271599769592, 114.44763994216919, 117.55831027030945, 124.43144106864929, 117.94856882095337, 123.27009797096252, 159.37689805030823, 178.44319701194763, 140.7037570476532]
print(len(respond_time_N100))
fig = plt.figure()
ax = fig.add_subplot(111)
major_ticks = np.arange(0, 100, 20)
minor_ticks = np.arange(0, 100, 5)
major_ticksy = np.arange(0, 200, 20)
minor_ticksy = np.arange(0, 200, 5)

ax.plot(respond_time_N10, label="Respond Time (N = 10)")
ax.plot(respond_times_N50, label="Respond Time (N = 50)")
ax.plot(respond_time_N100, label="Respond Time (N = 100)")
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticksy)
ax.set_yticks(minor_ticksy, minor=True)
# And a corresponding grid
ax.grid(which="both")
# Or if you want different settings for the grids:
ax.grid(which="minor", alpha=0.2)
ax.grid(which="major", alpha=0.5)
plt.xlabel("Number Of Transactions", fontsize=14)
plt.ylabel("Time (second)", fontsize=14)
plt.legend(loc="upper left")
plt.show()
