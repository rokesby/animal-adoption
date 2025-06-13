const GCP_CONFIG_PROD = {
    baseUrl: 'https://storage.googleapis.com',
    bucketName: 'pawsforacause-public',
    imageAssetsPath: 'assets/images'
}

export const buildImageUrl = (id, filename) => {
    const imageUrl = `${GCP_CONFIG_PROD.baseUrl}/${GCP_CONFIG_PROD.bucketName}/${GCP_CONFIG_PROD.imageAssetsPath}/${id}/${filename}`
    return imageUrl
};

