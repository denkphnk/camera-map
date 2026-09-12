import { useState } from "react";

import {
  ActionIcon,
  Box,
  Button,
  Center,
  Loader,
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

import { CameraCard } from "../../components/CameraList/CameraCard";
import { UploadModal } from "../../components/UploadModal/UploadModal";
import { CameraMarker } from "../../components/map/CameraMarker";

import { useGeoJson } from "../../hooks/useGeoJson";

import type { GeoJsonFeature } from "../../types/camera.types";

import classes from "./MapPage.module.css";

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

export function MapPage() {
  const [uploadOpened, setUploadOpened] = useState(false);

  const [selectedCameraId, setSelectedCameraId] =
    useState<string | null>(null);

  const {
    data,
    isLoading,
    isError,
  } = useGeoJson();

  const firstCamera = data?.features?.[0];

  return (
    <>
      <Box className={classes.page}>
        <Box className={classes.sidebar}>
          <Box className={classes.header}>
            <TextInput
              placeholder="Поиск камеры"
              leftSection={
                <IconSearch size={16} />
              }
            />

            <Box className={classes.actions}>
              <Button
                leftSection={
                  <IconUpload size={16} />
                }
                disabled={!selectedCameraId}
                onClick={() =>
                  setUploadOpened(true)
                }
              >
                Импорт видео
              </Button>

              <ActionIcon
                variant="light"
                size={36}
              >
                <IconFilter size={18} />
              </ActionIcon>
            </Box>
          </Box>

          <ScrollArea className={classes.list}>
            {isLoading && (
              <Center py="xl">
                <Loader />
              </Center>
            )}

            {isError && (
              <Center py="xl">
                <Text c="red">
                  Ошибка загрузки камер
                </Text>
              </Center>
            )}

            {!isLoading &&
              !isError &&
              data?.features && (
                <Stack gap="sm">
                  {data.features.map(
                    (
                      feature: GeoJsonFeature,
                    ) => (
                      <div
                        key={
                          feature.properties
                            .camera_id
                        }
                        onClick={() =>
                          setSelectedCameraId(
                            feature.properties
                              .camera_id,
                          )
                        }
                      >
                        <CameraCard
                          id={
                            feature.properties
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
              )}
          </ScrollArea>
        </Box>

        <Box className={classes.mapContainer}>
          <Map
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
                      setSelectedCameraId(
                        feature.properties
                          .camera_id,
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
        </Box>
      </Box>

      <UploadModal
        opened={uploadOpened}
        onClose={() =>
          setUploadOpened(false)
        }
      />
    </>
  );
}