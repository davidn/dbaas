# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'api_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'api_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'api.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'api_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'api.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'ClusterAudit'
        db.create_table(u'api_cluster_audit', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_clusters', on_delete=models.DO_NOTHING, to=orm['api.User'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=3306)),
            ('dbname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbusername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbpassword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backup_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=24)),
            ('backup_schedule', self.gf('django.db.models.fields.CharField')(default='3 */2 * * *', max_length=255)),
            ('iam_arn', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_key', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('ca_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'api', ['ClusterAudit'])

        # Adding model 'Cluster'
        db.create_table(u'api_cluster', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clusters', to=orm['api.User'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=3306)),
            ('dbname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbusername', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dbpassword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backup_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=24)),
            ('backup_schedule', self.gf('django.db.models.fields.CharField')(default='3 */2 * * *', max_length=255)),
            ('iam_arn', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_key', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('iam_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('ca_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_cert', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('client_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('server_key', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'api', ['Cluster'])

        # Adding model 'Provider'
        db.create_table(u'api_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'api', ['Provider'])

        # Adding model 'Region'
        db.create_table(u'api_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regions', to=orm['api.Provider'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('security_group', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'api', ['Region'])

        # Adding model 'Flavor'
        db.create_table(u'api_flavor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flavors', to=orm['api.Provider'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ram', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cpus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('free_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['Flavor'])

        # Adding model 'LBRRegionNodeSetAudit'
        db.create_table(u'api_lbrregionnodeset_audit', (
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_lbr_regions', on_delete=models.DO_NOTHING, to=orm['api.Cluster'])),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'api', ['LBRRegionNodeSetAudit'])

        # Adding model 'LBRRegionNodeSet'
        db.create_table(u'api_lbrregionnodeset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lbr_regions', to=orm['api.Cluster'])),
            ('lbr_region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('launched', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['LBRRegionNodeSet'])

        # Adding model 'NodeAudit'
        db.create_table(u'api_node_audit', (
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Cluster'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Region'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.Flavor'])),
            ('lbr_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_nodes', on_delete=models.DO_NOTHING, to=orm['api.LBRRegionNodeSet'])),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAxnWCcwsvgm7xEWOtaReDX+r+7jvwXNNnwC1E/sVPc6PhoPwX\nyZR61jkeBJeOlgqUHSaIdIPAb9K5mtxfTKnNS8SQVtNhpv6F4Ezym1W6/xPFkBz3\n6tqtg67lztlsGbmTozG6Ge3epqktTosobRmJXvAh6PZrst5xKB2NS8AD2vtQJ545\nVfeAi+JA9f8D1odLzBIpUBfFWhcwWMmmT9qjYY7Ty8u3xrDlLoQtDm0UewtJxvqe\nEzuXyqgzES/P8r0cIizyMH4FaKHTw2DmOgyvTrmXQrS6C5yqIjKRkYDzSZRf2tCX\nF1OcdES4RdRkvktE95JynUO8wQ1Pb3vjdJTkNQIDAQABAoIBAFVaUKJd2y8Du9Y4\nwmoCXNQx4zZevP+PRH3YemYAQi1//Bgak7h0jWf45Log3IgXQKBQ5DsINwlg3caG\npM358Xt2rIVLICKMMNPJBEZeVrBBtqRGcTGmnx2VaOzPgbiGocJ8LofcT/fppryz\nCM3zP6t/J3ZkFOm21X/lRdGgYYgZ78JOwuVXT+oVl42hUfdgcxgnEhBlQ+ZJP3CH\n4nehcF94tbyNj+NkC5y7bmmUhjuRtbgLfBKSCKoBHkWRQKstfNcGvoWDZa6MMr+0\nsE6CzXrL7f1NfJuN65nhzJHsDG1IpPWpA1Z6zXzsr8+QcUWju7/EKjrbNiiZsqF2\nc54XFgECgYEA1tt7rLmih9HvDNWfobee3hpqUq9qboINYeZHagvLInlQgKNXj/9X\nojjR4kzV1wSUmFJqBd0vT7XIUJplNaUg24ubWWs7pEs4bUeAfWyQwanoH6s9BTIU\nJT1abdAj9cQ1mHhJQ5+3nxr6O445L7C43tbRjyHw5TqiDbE2BmQ9KMECgYEA7HYq\nBbdSwyB1uQdsjn3aVADMmjvUs0DpsXCSOtEq4NQbU/bHWOgQhQTa03UI5oYj/oOA\n9BI+Y0GQAqoYBSC9xEMMtJQyPOmWgrHw3ebeZq5g34Cxgijo5HGg/IoeItaKQ4Wk\nU5lXLkUNs0O6qVhLMo/aB3Byo8GjaXWs8LtORHUCgYAOOnKyOYjd3bUq8Gql1vca\nVj18REmUD+C6/vjzuNw26DnAixCdZJd1ErYzekse9hqxC6Qhx0f+y1b8n3zcVJcc\nct5SyZslgiW2dum3ZJ0hdhL9JeXgljRnUuzOIN6AxAGYmz6ez9DlJHA1yXFYCyfy\n+d7ez6yYQY3Bwl6FhdXXAQKBgQDUWypSB9kjs7sFeE1diljQqAcXXDQg52L4H4iz\nmbVQRCxms3FDvuVXEI0U6j4cCMu6fo8Ionm02eRjAC6iLE1APJbkdVLIsV6h8PvH\nzNZekKwfDIxdwC+nOQTCx6dY0iNJkHOLQGKzAwDSxTiVbN3bgqTjmXDa78O5qhyt\n9QjNIQKBgG+5bkoTJ6gCLdSjFdPI7U/L/g/4EgE0z94Fzfk9ps7eSy/wd2RDDu/U\n4LRJhDJbXBBuldbibzp5NUrNZxtZwmH1p3s6qZtrLIlQEqGvajbmVl2LkV0DIDKL\nJWgoRsTF8TIMmEUpLy8y1R7I1q8QG2KNFXiGYLSCbAWLFo9oHKjv\n-----END RSA PRIVATE KEY-----')),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'api', ['NodeAudit'])

        # Adding model 'Node'
        db.create_table(u'api_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.Cluster'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.Region'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.Flavor'])),
            ('lbr_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['api.LBRRegionNodeSet'])),
            ('instance_id', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('security_group', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('health_check', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('nid', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('storage', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15, blank=True)),
            ('iops', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tinc_private_key', self.gf('django.db.models.fields.TextField')(default='-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA8o4RAZOKjAF4sohTmOzVyN+q/F4arSNrJnx66uzzpScvHXm+\nZGgswuu/p/IiVc4coiEtHX0lb6Z4bq0Dbzc9ll19V9L1Eyj9jSTSoUITkyEMVSCi\n9ujZ24ORd7065F/PxWQK5jnBu13TkPDVmKnLmd/RCzILQaQ39WwEJNJy3NqOKvr7\nmJrUNMGMTnhzCPdFc+sS/2LQ0Wg0AkJESo5Lf2yeq67LZ7WpJY0aZRY5E+QoSlUs\nfhQ6ALgQj/4F0peatiZb0i0ezGwX0q5VED7ZCv0migOVJS/CXaLB36Cd44oJVJFS\nboLC+bkXZTZEIcd6xtLqj6wt+GNfyzEwgqfiTwIDAQABAoIBAQCllZ6+eL6ofYis\nOKz5RRVdIHRV/NgxQnCvwWMYZdKe+HUNpkL3wLZuCwq32HDgKukZNZTbAMhBxF+L\nDsm9bvS4ZfJftkBgaCdP58dzFuzOEE2e/7zA2o1/cf4oxCIkLdRlaLqYGO3Mv2zj\nEcZ/hcrcrRLEldFhan5ZKPhbOt/3LFh90gDy0HutuexN73b6LnP0ejKVhZHswFWT\nOHAmKL0iKOOb1oS781e8MeeYsuplTYPH8VRavZ1/bIEN3TMnli0tBYfTFWF0uxUF\ngiTefAUE9kgNYfNa1T+TVoijK9qo4cnOr2+QCVwKGTLeaOjf3YLI+w/Hi41MLNIG\nDx8hqo2hAoGBAPREXXFlG+WRo/6t0pB880RhU+Cjc2N7FK2AOBVe4CX5MzPyVynf\nt47ojLlKGHuBQtDauafnIqOcN+8WP4LM6dglzq8EeeC0BuY3MNYYzhiYDMvXCe9M\nzm1wvHR69woeFjwf3wVIOi5PZJqo5q4O5X3FN+AfZwab9nXCAqvgM8FVAoGBAP40\npgPvyRjl9ibW2Pz5EVvCm7ve4B5K2LgV4if4g+ZWYJFavCDF8wyrINABOmAe4x1o\nNVhY3Fiipv3TYf5WTgn0mTKrtHPYvcJwH2QASv1e5KcfltZFdcG7CbW6mnAbn1Gb\n6dB1uMa5XDfBBuvr5CXBU306lEWkpa+tq3StYmUTAoGAMxtasa8F9zJRraeQtspt\n25DBi+6m5dmKqgJ5uX7wRwGsxOGfexNjxHLDfsER/kU9RZV94rNpe/HjghKVlzho\ndOD0LYoyNeF00BYcEa9+74ZgpwWG/pqDVkKQK47OwT8qR8ojT2edRLM3yWQtX52e\nRoJM/oeTdr6LAnhlNrDiI0ECgYBKN5jYwWNXD5zETingAd/diH3rZfDNJ1EKvejf\nfqET2Ngs1+7hKqoBYt0bnaArfBkW9tvMRXVfs21J4jNUDGKQaYdo0dTHldohMJcZ\nnTRHsTLU0FY7jOAKhc8Z7bc1T/s92mVzZUtjSa7w4DxjGOXtV/pGL5omkyGEnxHV\n6OE3XQKBgQC/aB5z6ZuC2lgDgbEjnpjHgkwBSg64Zd0UzzaW379TNWIYGY6lLpxK\nKjayIJGzqPRRHkX0FrMGloBJpZjGCTtCIre460hTQgY1lKVyUzU0siC0x6gr8BK2\nyAA+cCjS1H0X47FZHHNDZvrt7VfAGBR0qvYieHY7F/XoxxX/QZKvgQ==\n-----END RSA PRIVATE KEY-----')),
        ))
        db.send_create_signal(u'api', ['Node'])

        # Adding model 'Backup'
        db.create_table(u'api_backup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backups', to=orm['api.Node'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'api', ['Backup'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'api_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'api_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'api_user_user_permissions'))

        # Deleting model 'ClusterAudit'
        db.delete_table(u'api_cluster_audit')

        # Deleting model 'Cluster'
        db.delete_table(u'api_cluster')

        # Deleting model 'Provider'
        db.delete_table(u'api_provider')

        # Deleting model 'Region'
        db.delete_table(u'api_region')

        # Deleting model 'Flavor'
        db.delete_table(u'api_flavor')

        # Deleting model 'LBRRegionNodeSetAudit'
        db.delete_table(u'api_lbrregionnodeset_audit')

        # Deleting model 'LBRRegionNodeSet'
        db.delete_table(u'api_lbrregionnodeset')

        # Deleting model 'NodeAudit'
        db.delete_table(u'api_node_audit')

        # Deleting model 'Node'
        db.delete_table(u'api_node')

        # Deleting model 'Backup'
        db.delete_table(u'api_backup')


    models = {
        u'api.backup': {
            'Meta': {'object_name': 'Backup'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backups'", 'to': u"orm['api.Node']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'api.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['api.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        u'api.clusteraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ClusterAudit', 'db_table': "u'api_cluster_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'backup_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '24'}),
            'backup_schedule': ('django.db.models.fields.CharField', [], {'default': "'3 */2 * * *'", 'max_length': '255'}),
            'ca_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'client_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbpassword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dbusername': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'iam_arn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'iam_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3306'}),
            'server_cert': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server_key': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_clusters'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'api.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cpus': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'free_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flavors'", 'to': u"orm['api.Provider']"}),
            'ram': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'api.lbrregionnodeset': {
            'Meta': {'object_name': 'LBRRegionNodeSet'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lbr_regions'", 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'api.lbrregionnodesetaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LBRRegionNodeSetAudit', 'db_table': "u'api_lbrregionnodeset_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_lbr_regions'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Cluster']"}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'api.node': {
            'Meta': {'object_name': 'Node'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Cluster']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEAuYx5ejZ6qjKZhDsumNXvSWUNlmi1jETk22wwODk9WyGqT+IV\\nzXpEl/xcBHhmhdl5SR7LzZOmNVsN0LqxTqkf8Sd7v9yxHouAK+mO3xXgGdRl0lX+\\ntPtGUPXYpRxkol31K1X66v+CBosi/yjAmy7qX3L1QRL+sPdQVJzSx1I2bbNS0Kjc\\nc0AAkr91hfvmICkGKW1JLZJ5H/rL07qOCeY4B9GPc9c0S31cMG/yhquGIoLqxX3J\\n6p8qxKmcjlXkOM5qFylVwWzceqm/YFS8M4pn98xZQfc/HrUbZb+jAhSHAlO6qZte\\nIFWClEkpNOtI1CP54dBg1JepkobiII0OkvqaOwIDAQABAoIBACvbs38az4XZbgYe\\ngxYnQ2di1oJd/8PHKR1ghklT5lfbLkmxlBu8segHA60e1IUA8bVB7USLiPcFrc9P\\nwcdpHJ7BCXRBczBYIxS+IUJEBnO0i9ja8NjQqD9MzUfB3Vuvv9rdePEBMjffvYb4\\nmAZWYZnsL2KRXdhwrPFDHGN24FyvZmoWL7qJ2s484ygYgg7Uix1Q9BjC4WPbzrrq\\nHS386Jz0Cp0rtXO72RoUBu1lrRH1U3ixZu+nvY0yHV5jBXrSZxR6u8aC12d3sSpX\\nQzc9k+15jquoU7PxTzZd9zYsYNN9qKs6hUaF1MN1ZrQmt+Jp3w7W5H0Y1orFVWwO\\nD+SdILECgYEA0/aqobdsF/lI0850Qcq0ZhG4sb32N2+8KJFAEr1sPaTfWREYIJHR\\nBAZB3om+H9p4EgalKmHIHl+Er9MfY0zMrXmJ4NH1WWvwMhTlLK5mtCRc7ZcI+iIc\\n6I6NDB538o8C7izAQUh4gctYKgzfVPGG7dDgmiOQvMCtN3lRbwqHR2MCgYEA4Bjt\\n/Nly4WBOVeFx00+UOTSshSnKISdTZp1n0pHEcxe6DHTabvCiAIN3Ytd8khjfFFZB\\nyFGuuOREABMbVmdfjhCP98xwSqZt63UsNYd5Foy67JkMyVpxpDqdCd9v+hozbg/E\\nN1mJ9OGxt47QLbTf0d4JyD6/C0y0XWfVDIJNdUkCgYBsM7wRB6A/cLrznK2ONFr4\\ny80bttwsmnZTwyoRJu9NXI/DWM2XOriXNFaFso0Cl7S5hvjjdL0CfEIwuzaHq1nE\\nqIlw4d08Q7R+7Fm9AF5fUTy68GHdxnI5aSOpbxhOEyEs0l1mNgeGQnaEKMQNCaqW\\nVg2BwewN3tHNwrmGVLqP/wKBgDyjwlJ3bPS7oLbwiGKL2CoarMxj4IRUJedQlLWQ\\nKD6Unw2b2TfH+a515KpkcRr/i+3u4WIZaFQzwIrcoLsiweKpbKu7MG+i1X+vd0UM\\n4aFOd45qY+FgjfvIuJHhWmWtDVms/oWTvxb6s6JeDMsxdJdPpAoBoKSoHu5fmHEI\\nGXmxAoGAFv1Rv6N9KsRyJLsLKXKWKI+JkkNYiMGDsefF/jL1EsymfwaZmz3Lm7/K\\nNNCp749SyprNxIevoQU5gdpzUDY97XQELR3w5UHUFyhAg1M2aVJquUrZMZKDuRDX\\ns3OC2/v3r/vM0unVCVv0onaKYC7WQn9SWw4rAszjy4FQDxft57g=\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.nodeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'NodeAudit', 'db_table': "u'api_node_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Cluster']"}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Flavor']"}),
            'health_check': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'instance_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'iops': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lbr_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.LBRRegionNodeSet']"}),
            'nid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nodes'", 'on_delete': 'models.DO_NOTHING', 'to': u"orm['api.Region']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'storage': ('django.db.models.fields.IntegerField', [], {}),
            'tinc_private_key': ('django.db.models.fields.TextField', [], {'default': "'-----BEGIN RSA PRIVATE KEY-----\\nMIIEpQIBAAKCAQEAstQmA4zUmnv/Ie9/c/FByeQ8VcaGJXFoCI2KkYPdJoisYPGE\\nA/bQ4MNIxcRpj+mwLaLWPqTn03FR1jftUOyeC+XCH0CSKflIpZHnIPvMSa3WcEpy\\nP9H+MAmeulfQ1SW3whjXmxqraLfhCI+9yvAXg7/rw9JoEc6donBhWiUpBcOPmKcs\\nHwZ2H8gRJjebfY14srNQqC65Sy6HZHt8Roy9EBGadiikFbYd5GeickVut2PWGn9Y\\nnPYoSVGEQq6VxhZNB+jPtTbR+aqrRkNCrQ1VckbXdJc3u8KMmd85o1f58UIny4uy\\nRHkaracNmkR3/WGSWddnGOZPe1KVOu6/OWOO8wIDAQABAoIBADbbbW3ZXb6mGvXG\\nCkr+zzenk/qcE7qYt1koUkGhOc4ATyDN9blhlWHdhg1k2x0SisD1GtPMsnDiakBU\\nl7AjZbgwmwQLQsstdWOVBlnP5DMV6Jo5vCJnwJnr2Y1AMwevslcQV9N0svBEt/tw\\nXMBMNmpsDV7cxJ/xydlyr+p/S75AYuLfb/HNjJRng5FpeBVp+Gd9aWhZdTtLOKWv\\nGgkO+2by71p1W+xsl1BH6hRXlHN97/mBsvy5iERYtUN3t58sImYVkUhvmzxCTsNg\\nDNLRtOXUZ0b4e8M/JxiVv2Z5tk2xMTPLwzXJUQVX5+JjadgJ11uKmyn8X0qQOVdi\\nKiubyUECgYEAupCN7ZK8bfq9yrvrMaw/6ZRSWwrEyEq61XBiwIgHHtGRZ1QFPXyL\\ntwN7jr0YaZtds0rs9cDrSiufYkzEV/CJluT5PdOC07WGVPCKoMli5/dfHkTt3SUt\\ntU088ZRn3CIa1pT5Skm/HZq87tYPpjDcc/OeLYZHVhYratFGokLF8+0CgYEA9WKH\\nosXGo8cQSSdoTofUDjvy7Zh80XadnZFjNEE1Y7Hw489B+4KLO5+iFs++LMy9DQSF\\n5pkOXpn3FA2WXOszP9Y6WcbMSyEHKfLsEwfZMJFM0MbxIzmjewIa5WTm/Tfh9Skp\\n5mF0u2J2onSaiLbGUstA+8fnsXz/LsxTCBu48l8CgYEAtx98sFz/p9Qexwh9a1xv\\nv45e6A5B6XewvCB8Tg83LgD2gD3whtHhMdqxRQJHHCHsbzh0LyUVzs/SumIvt0Hb\\nS8mk/BLIr5XWLTmOWRRTiO0+6C8wa4k6vGL8FwRcja7MOSQxLcIFXcGtAaIL6ky7\\nlvThpj3Pd6h7JXYVpt9z/mECgYEApKrBEIcd/MvZ7u1l/sUBlae/Jpgcssehj5p/\\n8xILTOKdH5L22VvKKXG/aQVxvkiKWRD+9jchwHQbrTZM///JvX36XEKe14/Laegd\\nacvrgL8QyE2ohhXo0eQgvm2O4MA+frFn77TYi+LQb8ZF6ZaV0fuZmRyWK7IQ4Iu2\\n8IsB+osCgYEAh40y62xhfPfq73q3etcKZBtmPxz0/6B/w2BF1BkW/on5TbshZpaO\\nhGVR8z/zazJRRpyuYrhTf4w04DCtGzl+MLN0na9TKuqQaaaNFlC4v1dVayuyEise\\nFPqM/R7/Oi+rp0meFQGh2R2pIsHHpH4/0z2g3OS+RbBjjYdUr0cu+jg=\\n-----END RSA PRIVATE KEY-----'"})
        },
        u'api.provider': {
            'Meta': {'object_name': 'Provider'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'key_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'lbr_region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'to': u"orm['api.Provider']"}),
            'security_group': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']