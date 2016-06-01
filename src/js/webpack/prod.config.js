var path = require('path')
var webpack = require('webpack')

module.exports =
{ devtool: 'source-map'
, entry:
  { 'main': './js/index'
  }
, output:
  { path: path.join(__dirname, '..', '..', '..', 'build', 'website')
  , filename: 'bundle.js'
  }
, plugins:
  [ new webpack.IgnorePlugin(/\.\/dev/, /\/config$/)
  , new webpack.DefinePlugin(
    { 'process.env':
      { NODE_ENV: JSON.stringify('production')
      }
    })
  , new webpack.optimize.DedupePlugin()
  , new webpack.optimize.UglifyJsPlugin(
    { compress:
      { warnings: false
      }
    })
  , new webpack.DefinePlugin(
    { __DEV__: JSON.stringify(JSON.parse(process.env.BUILD_DEV || 'true'))
    , __PRERELEASE__: JSON.stringify(JSON.parse(process.env.BUILD_PRERELEASE || 'false'))
    })
  ]
, module:
  { loaders:
    [ { test: /\.js$/
      , loaders: ['babel']
      , exclude: /node_modules/
      , include: path.join(__dirname, '..')
      }
    , { test: /\.json$/
      , loader: 'json-loader?paths=/src/js/'
      }
    , { test: /\.styl$/
      , loader: 'style!css!stylus'
      , exclude: /node_modules/
      }
    ]
  }
}
