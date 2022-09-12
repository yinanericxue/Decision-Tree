import trees
import treePlotter

lenses = [ inst.strip().split('\t') for values in open('lenses.txt').readlines() ]
labels = ['age','prescript','astigmatic','tearRate']
tree = trees.createTree(lenses,labels)
treePlotter.createPlot(tree)
