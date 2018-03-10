class Tag < ApplicationRecord
  has_many :combinations, dependent: :destroy
  has_many :microposts, through: :combinations
  has_many :users, through: :microposts
  validate :name, presence: true, length: { maximum: 50 }
end
