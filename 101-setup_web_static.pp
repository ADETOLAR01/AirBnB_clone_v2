# web_static_setup.pp

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html><body>Test Page</body></html>',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership recursively
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  ensure => file,
  source => 'puppet:///modules/mymodule/default',
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
