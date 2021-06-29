from graphviz import Digraph

# 获取所有节点中最多子节点的叶节点
def getMaxLeafs(myTree):
    numLeaf = len(myTree.keys())
    for key, value in myTree.items():
        if isinstance(value, dict):
            sum_numLeaf = getMaxLeafs(value)
            if sum_numLeaf > numLeaf:
                numLeaf = sum_numLeaf
    return numLeaf

def plot_model(tree, name):
    g = Digraph("G", filename=name, format='png', strict=False)
    # g.graph_attr["size"] = "16,8"
    g.attr(width="1500pt", height="1000pt", fixedsize='true',fontsize='18')
    first_label = list(tree.keys())[0]
    g.node("0", first_label)
    g.node_attr.update(fontsize='18',width='1')
    _sub_plot(g, tree, "0")
    leafs = str(getMaxLeafs(tree) // 10)
    g.attr(rankdir='LR',ranksep=leafs)
    g.edge_attr.update(arrowhead='vee', arrowsize='1',fontsize='18',labelfontsize='18')
    g.view()

root = "0"

def _sub_plot(g, tree, inc):
    global root

    first_label = list(tree.keys())[0]
    ts = tree[first_label]
    for i in ts.keys():
        if isinstance(tree[first_label][i], dict):
            root = str(int(root) + 1)
            g.node(root, list(tree[first_label][i].keys())[0])
            g.edge(inc, root, str(i))
            _sub_plot(g, tree[first_label][i], root)
        else:
            root = str(int(root) + 1)
            color_dict = {'0.65':'seashell','0.66':'mistyrose','0.68':'pink','0.69':'lightcoral',
                          '0.72':'lightcoral','0.74':'salmon','0.75':'orangered','0.76':'red',
                          '0.78':'maroon','0.79':'indianred','0.80':'brown','0.81':'brown',
                          '0.82':'firebrick','0.83':'firebrick'}
            key = str(tree[first_label][i]).split('|')[1]
            g.node(root, str(tree[first_label][i]),color=color_dict[key],style='filled')
            g.edge(inc, root, str(i))

tree = {
 "turnover_rate<0.04": {
  "Yes": {
   "turnover_rate<-0.42": {
    "Yes": {
     "volume_ratio<-0.14": {
      "Yes": {
       "turnover_rate<-0.84": {
        "Yes": {
         "free_share<0.42": {
          "Yes": '6|0.80',
          "No": '4|0.79'
         }
        },
        "No": {
         "bps_yoy<0.15": {
          "Yes": {
           "free_share<-0.15": {
            "Yes": '5|0.68',
            "No": '3|0.82'
           }
          },
          "No": {
           "dv_ttm<0.18": {
            "Yes": '5|0.75',
            "No": '8|0.74'
           }
          }
         }
        }
       }
      },
      "No": {
       "dv_ttm<0.06": {
        "Yes": {
         "bps_yoy<0.09": {
          "Yes": '7|0.78',
          "No": '5|0.65'
         }
        },
        "No": {
         "total_share<-0.12": {
          "Yes": '2|0.78',
          "No": '3|0.78'
         }
        }
       }
      }
     }
    },
    "No": {
     "total_share<-0.17": {
      "Yes": {
       "free_share<-0.41": {
        "Yes": {
         "dv_ttm<-0.2": {
          "Yes": {
           "volume_ratio<-0.31": {
            "Yes": '8|0.66',
            "No": '6|0.83'
           }
          },
          "No": '1|0.82'
         }
        },
        "No": {
         "total_share<-0.23": {
          "Yes": {
           "volume_ratio<-0.24": {
            "Yes": '7|0.78',
            "No": '4|0.78'
           }
          },
          "No": {
           "dv_ttm<-0.07": {
            "Yes": '4|0.82',
            "No": '7|0.81'
           }
          }
         }
        }
       }
      },
      "No": {
       "turnover_rate<-0.23": {
        "Yes": '3|0.78',
        "No": '4|0.79'
       }
      }
     }
    }
   }
  },
  "No": {
   "free_share<-0.37": {
    "Yes": {
     "bps_yoy<0.21": {
      "Yes": {
       "bps_yoy<-0.42": {
        "Yes": '10|0.72',
        "No": '3|0.83'
       }
      },
      "No": {
       "bps_yoy<1.01": {
        "Yes": '9|0.79',
        "No": '7|0.66'
       }
      }
     }
    },
    "No": {
     "turnover_rate<0.7": {
      "Yes": {
       "free_share<-0.09": {
        "Yes": '2|0.76',
        "No": '6|0.81'
       }
      },
      "No": '1|0.69'
     }
    }
   }
  }
 }
}

plot_model(tree, "tree2.gv")

# 20160630  20181231