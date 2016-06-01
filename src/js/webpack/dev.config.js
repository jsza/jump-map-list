var path = require('path')
var webpack = require('webpack')
var autoprefixer = require('autoprefixer')

module.exports =
{ devtool: '#cheap-module-eval-source-map'
, entry:
  [ 'webpack-dev-server/client?http://localhost:3001'
  , 'webpack/hot/only-dev-server'
  , path.join(__dirname, '..', 'index.js')
  ]
, output:
  { path: path.join(__dirname, 'dist')
  , filename: 'bundle.js'
  , publicPath: 'http://localhost:3001/static/js/'
  }
, plugins:
  [ new webpack.HotModuleReplacementPlugin()
  , new webpack.DefinePlugin(
    { __DEV__: JSON.stringify(JSON.parse(process.env.BUILD_DEV || 'true'))
    , __PRERELEASE__: JSON.stringify(JSON.parse(process.env.BUILD_PRERELEASE || 'false'))
    })
  ]
, module:
  { loaders:
    [ { test: /\.js$/
      , loaders: ['react-hot', 'babel']
      , exclude: /node_modules/
      , include: path.join(__dirname, '..')
      }
    , { test: /\.json$/
      , loader: 'json-loader?paths=/js/'
      }
    , { test: /\.styl$/
      , loader: 'style!css!stylus'
      // , include: path.join(__dirname, '..')
      , exclude: /node_modules/
      }
    ]
  , noParse: [/\.md$/]
  }
// , postcss:
//   [ autoprefixer(
//       { browsers: ['last 2 versions']
//       })
//   ]
, devServer:
  { headers: { 'Access-Control-Allow-Origin': '*' }
  , inline: true
  }
, node:
  { fs: 'empty'
  , tls: 'empty'
  }
}
