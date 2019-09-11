from rest_framework import serializers
from .models import Band, Player, Instrument, Venue, Festival, Album

base_fields = ('name', 'url', 'id', 'description', 'country', 'external_URL', 'thumbnail')


class BandSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:band-detail',
    )
	class Meta:
		model = Band
		fields = base_fields + ('members', 'isactive', 'festival', 'venue', 'album')


class InstrumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instrument
		fields = ('name',)

class PlayerSerializer(serializers.ModelSerializer):
	instrument = InstrumentSerializer(many=True)
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:player-detail',
    )

	class Meta:
		model = Player
		fields = base_fields + ('instrument', 'band', 'isactive', 'festival', 'venue', 'album', 'gigged_with')



class FestivalSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:festival-detail',
    )
	class Meta:
		model = Festival
		fields =  base_fields + ('isactive', 'bandsplayed', 'playersplayed')


class VenueSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:venue-detail',
    )
	class Meta:
		model = Venue
		fields = base_fields + ('isactive', 'bandsplayed', 'playersplayed')


class AlbumSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:album-detail',
    )
	class Meta:
		model = Album
		fields = base_fields + ('date', 'band', 'playersplayed')



class LinkPlayerSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:player-detail',
    )

	class Meta:
		model = Player
		fields = ('id', 'url', 'band', 'festival', 'venue', 'album', 'gigged_with')

class LinkBandSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
        view_name='DjangoVerse:band-detail',
    )
	class Meta:
		model = Band
		fields = ('id', 'url', 'festival', 'venue', 'album')



# Unique country serialisation

class BandCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Band
		fields = ('country',)

class PlayerCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = ('country',)

class FestivalCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Festival
		fields = ('country',)

class VenueCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Venue
		fields = ('country',)

class AlbumCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Album
		fields = ('country',)