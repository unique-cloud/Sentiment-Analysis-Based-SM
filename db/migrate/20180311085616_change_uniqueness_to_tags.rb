class ChangeUniquenessToTags < ActiveRecord::Migration[5.1]
  def change
    change_column :tags, :name, :string, unique: true
  end
end
