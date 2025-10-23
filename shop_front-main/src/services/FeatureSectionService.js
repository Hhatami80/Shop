import api from './AxiosService'

export function fetchFeatureSection() {
  return api.get('/feature-section')
}

export function updateFeatureSection(payload) {
  return api.put('/feature-section-update/', payload)
}
