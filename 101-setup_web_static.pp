# Install Puppet on your web servers if it is not already installed:
sudo apt-get update
sudo apt-get install puppet -y

sudo nano /etc/puppet/modules/web_static/manifests/0-setup_web_static.pp

# sudo puppet module install puppetlabs-nginx
sudo puppet module install puppetlabs-nginx

# Install Nginx
class { 'nginx': }

# Create necessary directories
file { '/data':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

file { '/data/web_static':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

file { '/data/web_static/releases':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

file { '/data/web_static/shared':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
    content => '<html><head></head><body>Holberton School</body></html>',
    ensure  => 'file',
    owner   => 'ubuntu',
    group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test/',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data/web_static/releases/test'],
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
    content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
",
    ensure => 'file',
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
}

# Restart Nginx
service { 'nginx':
    ensure    => 'running',
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
}

sudo puppet apply /etc/puppet/modules/web_static/manifests/0-setup_web_static.pp
