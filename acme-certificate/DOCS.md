# Home Assistant Add-on: acme.sh-Certificate add-on

## How to use

This addon uses the acme.sh script to create SSL certificates.
You can create multiple certificates with this add-on.

## Configuration

Here is an example that creates a Certificate that responds to two domains, XYZZYha.duckdns.org and XYYZZYhal.duckdns.org.

XYZZYha is used for the Internet and XYZZYhal is used on my LAN.

For details of acme.sh options see: https://github.com/acmesh-official/acme.sh/blob/master/README.md

**Note**: _Remember to restart the add-on when the configuration is changed._

```yaml
email: xyzzy@gmail.com
config_sub_dicrectory: acme
domains:
  - domain: XYZZYha.duckdns.org
    issue_options:
      - "-d XYZZYhal.duckdns.org"
      - "--dns dns_duckdns"
      - "--server letsencrypt"
    deploy_options:
      - "--deploy-hook localcopy"
    environment:
      - DuckDNS_Token=12345678-1234-5678-90ab-1234567890ab
      - DEPLOY_LOCALCOPY_CERTKEY="/ssl/privkey.pem"
      - DEPLOY_LOCALCOPY_FULLCHAIN="/ssl/fullchain.pem"
```

### Option `email`

This email address is used by the CA (letsencrypt, zerossl, ...) to associate with your certificates.

### Option `config_sub_dicrectory`

A directory with this name is created in your Home Assistant config director. This contains information needed to renew your certificates as well as configuration and log files.

### Option `domains`

The list of primary certificate domains. This is an array, 1 per certificate.
The format of each entry is as follows:

#### Option `domain`

The primary domain name for the certificate.

#### Option `issue_options`

A list of extra command line arguments used to issue the certificate.

#### Option `deploy_options`

A list of extra command line arguments used to deploy the certificate.

#### Option `environment`

A list of environment variables used to provide additional arguments to the acme.sh script



