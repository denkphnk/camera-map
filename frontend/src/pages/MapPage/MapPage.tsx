import { useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
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

const MAPBOX_TOKEN =
  import.meta.env.VITE_MAPBOX_TOKEN;

export function MapPage() {
  const [uploadOpened, setUploadOpened] =
    useState(false);

  const [
    selectedCameraId,
    setSelectedCameraId,
  ] = useState<string | null>(null);

  const [search, setSearch] =
    useState("");

  const [model, setModel] =
    useState("");

  const [cameraType, setCameraType] =
    useState("");

  const [cameraClass, setCameraClass] =
    useState("");

  const [videoFrom, setVideoFrom] =
    useState("");

  const [videoTo, setVideoTo] =
    useState("");

  const navigate = useNavigate();

  const mapRef =
    useRef<MapRef>(null);

  const {
    data,
    isLoading,
    isError,
  } = useGeoJson();

  const firstCamera =
    data?.features?.[0];

  const filteredFeatures =
    useMemo(() => {
      if (!data?.features) {
        return [];
      }

      const query =
        search.trim().toLowerCase();

      return data.features.filter(
        (
          feature: GeoJsonFeature,
        ) => {
          const p =
            feature.properties;

          const searchMatch =
            !query ||
            p.camera_id
              .toLowerCase()
              .includes(query) ||
            (p.address ?? "")
              .toLowerCase()
              .includes(query) ||
            (p.camera_name ?? "")
              .toLowerCase()
              .includes(query);

          const modelMatch =
            !model ||
            (p.model ?? "")
              .toLowerCase()
              .includes(
                model.toLowerCase(),
              );

          const typeMatch =
            !cameraType ||
            (
              p.camera_type ?? ""
            )
              .toLowerCase()
              .includes(
                cameraType.toLowerCase(),
              );

          const classMatch =
            !cameraClass ||
            (
              p.camera_class ?? ""
            )
              .toLowerCase()
              .includes(
                cameraClass.toLowerCase(),
              );

          const fromMatch =
            !videoFrom ||
            p.video_count >=
              Number(videoFrom);

          const toMatch =
            !videoTo ||
            p.video_count <=
              Number(videoTo);

          return (
            searchMatch &&
            modelMatch &&
            typeMatch &&
            classMatch &&
            fromMatch &&
            toMatch
          );
        },
      );
    }, [
      data,
      search,
      model,
      cameraType,
      cameraClass,
      videoFrom,
      videoTo,
    ]);

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
                  value={search}
                  onChange={(event) =>
                    setSearch(
                      event.currentTarget.value,
                    )
                  }
                  placeholder="Поиск камеры"
                  leftSection={
                    <IconSearch size={16} />
                  }
                />

                <TextInput
                  value={model}
                  onChange={(event) =>
                    setModel(
                      event.currentTarget.value,
                    )
                  }
                  placeholder="Модель камеры"
                />

                <TextInput
                  value={cameraType}
                  onChange={(event) =>
                    setCameraType(
                      event.currentTarget.value,
                    )
                  }
                  placeholder="Тип камеры"
                />

                <TextInput
                  value={cameraClass}
                  onChange={(event) =>
                    setCameraClass(
                      event.currentTarget.value,
                    )
                  }
                  placeholder="Класс камеры"
                />

                <Group grow>
                  <TextInput
                    value={videoFrom}
                    onChange={(event) =>
                      setVideoFrom(
                        event.currentTarget.value,
                      )
                    }
                    placeholder="Видео от"
                  />

                  <TextInput
                    value={videoTo}
                    onChange={(event) =>
                      setVideoTo(
                        event.currentTarget.value,
                      )
                    }
                    placeholder="Видео до"
                  />
                </Group>

                <Button
                  color="gray"
                  variant="light"
                  onClick={() => {
                    setSearch("");
                    setModel("");
                    setCameraType("");
                    setCameraClass("");
                    setVideoFrom("");
                    setVideoTo("");
                  }}
                >
                  Сбросить фильтры
                </Button>

                <Button
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
                      Ошибка загрузки камер
                    </Text>
                  </Center>
                )}

                {!isLoading &&
                  !isError &&
                  filteredFeatures.map(
                    (
                      feature: GeoJsonFeature,
                    ) => (
                      <div
                        key={
                          feature.properties
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
                            feature.properties.db_id
                          }
                          id={
                            feature.properties.camera_id
                          }
                          address={
                            feature.properties.address ??
                            "Адрес не указан"
                          }
                          latitude={
                            feature.geometry.coordinates[1]
                          }
                          longitude={
                            feature.geometry.coordinates[0]
                          }
                          camerasCount={
                            feature.properties.video_count
                          }
                          onDetails={() =>
                            navigate(
                              `/cameras/${feature.properties.db_id}`,
                            )
                          }
                        />
                      </div>
                    ),
                  )}

                {!isLoading &&
                  !isError &&
                  filteredFeatures.length ===
                    0 && (
                    <Center py="xl">
                      <Text c="dimmed">
                        Камеры не найдены
                      </Text>
                    </Center>
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
            {filteredFeatures.map(
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