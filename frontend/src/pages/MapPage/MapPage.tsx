import { useRef, useState } from "react";

import {
  ActionIcon,
  Button,
  Center,
  Group,
  Loader,
  Paper,
  ScrollArea,
  Stack,
  Text,
  TextInput,
} from "@mantine/core";

import {
  IconFilter,
  IconSearch,
  IconUpload,
} from "@tabler/icons-react";

import Map from "react-map-gl/mapbox";
import { Marker } from "react-map-gl/mapbox";
import type { MapRef } from "react-map-gl/mapbox";

import { CameraCard } from "../../components/CameraList/CameraCard";
import { UploadModal } from "../../components/UploadModal/UploadModal";
import { CameraMarker } from "../../components/map/CameraMarker";

import { useGeoJson } from "../../hooks/useGeoJson";

import type { GeoJsonFeature } from "../../types/camera.types";

import classes from "./MapPage.module.css";

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

export function MapPage() {
  const [uploadOpened, setUploadOpened] =
    useState(false);

  const [
    selectedCameraId,
    setSelectedCameraId,
  ] = useState<string | null>(null);

  const mapRef =
    useRef<MapRef>(null);

  const {
    data,
    isLoading,
    isError,
  } = useGeoJson();

  const firstCamera =
    data?.features?.[0];

  function handleSelectCamera(
    feature: GeoJsonFeature,
  ) {
    setSelectedCameraId(
      feature.properties.db_id,
    );

    mapRef.current?.flyTo({
      center: [
        feature.geometry.coordinates[0],
        feature.geometry.coordinates[1],
      ],
      zoom: 15,
      duration: 1000,
    });
  }

  return (
    <>
      <div className={classes.page}>
        <Paper
          withBorder
          radius={0}
          className={classes.sidebar}
        >
          <Stack h="100%" gap={0}>
            <Paper
              withBorder
              radius={0}
              p="md"
            >
              <Stack>
                <TextInput
                  placeholder="Поиск камеры"
                  leftSection={
                    <IconSearch size={16} />
                  }
                />

                <Group>
                  <Button
                    flex={1}
                    color="violet"
                    leftSection={
                      <IconUpload size={16} />
                    }
                    disabled={
                      !selectedCameraId
                    }
                    onClick={() =>
                      setUploadOpened(
                        true,
                      )
                    }
                  >
                    Импорт видео
                  </Button>

                  <ActionIcon
                    size={36}
                    variant="light"
                    color="violet"
                  >
                    <IconFilter size={18} />
                  </ActionIcon>
                </Group>
              </Stack>
            </Paper>

            <ScrollArea flex={1}>
              <Stack p="md">
                {isLoading && (
                  <Center py="xl">
                    <Loader />
                  </Center>
                )}

                {isError && (
                  <Center py="xl">
                    <Text c="red">
                      Ошибка загрузки
                      камер
                    </Text>
                  </Center>
                )}

                {!isLoading &&
                  !isError &&
                  data?.features?.map(
                    (
                      feature: GeoJsonFeature,
                    ) => (
                      <div
                        key={
                          feature
                            .properties
                            .camera_id
                        }
                        onClick={() =>
                          handleSelectCamera(
                            feature,
                          )
                        }
                      >
                        <CameraCard
                          selected={
                            selectedCameraId ===
                            feature
                              .properties
                              .db_id
                          }
                          id={
                            feature
                              .properties
                              .camera_id
                          }
                          address="Адрес камеры"
                          latitude={
                            feature.geometry
                              .coordinates[1]
                          }
                          longitude={
                            feature.geometry
                              .coordinates[0]
                          }
                          camerasCount={1}
                        />
                      </div>
                    ),
                  )}
              </Stack>
            </ScrollArea>
          </Stack>
        </Paper>

        <div
          className={
            classes.mapContainer
          }
        >
          <Map
            ref={mapRef}
            className={classes.map}
            mapboxAccessToken={
              MAPBOX_TOKEN
            }
            mapStyle="mapbox://styles/mapbox/streets-v12"
            initialViewState={{
              latitude:
                firstCamera?.geometry
                  .coordinates[1] ??
                55.751244,

              longitude:
                firstCamera?.geometry
                  .coordinates[0] ??
                37.618423,

              zoom: 11,
            }}
          >
            {data?.features.map(
              (
                feature: GeoJsonFeature,
              ) => (
                <Marker
                  key={
                    feature.properties
                      .camera_id
                  }
                  longitude={
                    feature.geometry
                      .coordinates[0]
                  }
                  latitude={
                    feature.geometry
                      .coordinates[1]
                  }
                >
                  <div
                    onClick={() =>
                      handleSelectCamera(
                        feature,
                      )
                    }
                  >
                    <CameraMarker
                      hasVideo={
                        feature.properties
                          .has_video
                      }
                    />
                  </div>
                </Marker>
              ),
            )}
          </Map>
        </div>
      </div>

      <UploadModal
        opened={uploadOpened}
        onClose={() =>
          setUploadOpened(false)
        }
        cameraId={
          selectedCameraId ?? ""
        }
      />
    </>
  );
}