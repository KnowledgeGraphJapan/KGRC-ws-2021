from rdflib import URIRef
import pandas
import pydotplus
from IPython.display import (
  display, 
  Image, 
  SVG,
)
from rdflib.tools.rdf2dot import rdf2dot
from rdflib import (
  Graph,
  URIRef
)

from traceback import print_exc
import io
import re
import os
import tempfile

def load_rdf_files(graph, filenames):
  for filename in filenames:
    graph.parse(filename)
  return graph


def insert(graph, triples):
  for triple in triples:
    graph.add(triple)
  return graph


def flatten(lists):
  flat_list = []
  for l in lists:
    flat_list.extend(l)
  return flat_list


def extract_rule(query):
  lines = [re.sub(r'#.*$', '', line) for line in query.strip().split('\n')]
  lines = list(filter(lambda line:len(line)>0, lines))
  return  re.sub(r'^[^\{]+(\{.*\})[^\}]*$', r'\1', ''.join(lines))


def get_value_from_sparql_result(results, key):
  return [b[key] for b in results.bindings]


def get_scene(g, idx=1):
  q = f'''
        PREFIX kd:<http://kgc.knowledge-graph.jp/data/SpeckledBand/>
        SELECT DISTINCT ?predicate ?object {{
          {idx} ?predicate ?object.
        }}
      '''
  return g.query(q)


def create_print_scene(g):
  def _print_scene(idx):
    return pretty_print(get_scene(g, idx), g.namespace_manager)
  return _print_scene


def pretty_print(res, namespace_manager):
  vars = res.vars
  def replace_with_prefix(di):
    new_di = dict()
    for k, v in di.items():
      new_di[k] = v.n3(namespace_manager)
    return new_di
  values = [replace_with_prefix(b) for b in res.bindings]
  df = pandas.DataFrame(values, columns=vars)
  from IPython.display import display
  display(df)

  
def print_dot(dot):
  binary_image = pydotplus.graph_from_dot_data(dot).create_svg()
  display(SVG(binary_image))

  
def print_ttl(ttl, prefixes=None):
  
  def print_g(g):
    stream = io.StringIO()
    rdf2dot(g, stream, opts = {display})
    dot = stream.getvalue()
    print_dot(dot)

  if os.path.isfile(ttl) and ttl.rsplit('.')[-1] == 'ttl':
    with open(ttl) as fp:
      content = ''.join(fp)
    if prefixes is not None:
      content = f'{prefixes} \n {content}'
      print('sss')
  else:
    default_prefixes = '''
      @prefix : <http://kgchallenge.github.io/ontology/project/0PySb2LTgsogxpMGxkXdS#> .
      @prefix owl: <http://www.w3.org/2002/07/owl#> .
      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .    
      @prefix xml: <http://www.w3.org/XML/1998/namespace> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

      @prefix kgc: <http://kgc.knowledge-graph.jp/ontology/kgc.owl#> .
      @prefix kd: <http://kgc.knowledge-graph.jp/data/SpeckledBand/> .

      @prefix kgcf: <http://kgchallenge.github.io/ontology/> .
      @prefix kdf: <http://kgchallenge.github.io/data/#> .
      @prefix ns1: <file:///tmp/tmpnbl_fm0z#> .

      @base <http://kgchallenge.github.io/ontology/project/0PySb2LTgsogxpMGxkXdS> .
    '''
    content = ttl
    
    if prefixes is None:
      prefixes = default_prefixes
    content = f'{prefixes} \n {content}'
    
  g = Graph()
  with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tfp:
    tfp.write(content)
    tfp.flush()
    g.parse(tfp.name, format='ttl')
  print_g(g)